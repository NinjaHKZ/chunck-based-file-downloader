import aiohttp, asyncio, json, os, time
import subprocess, atexit

async def _Downloader(url, vidName) -> dict:
	if f'{vidName}.mp4' in os.listdir():
		print(f'o arquivo desejado já existe, caso queira baixar novamente o arquivo "{vidName}.mp4"')
		return {"Fail": {'File': 'O arquivo já existe', 'ID-code': 0}}

	elif f'{vidName}.mp4' not in os.listdir():
		if f'{vidName}.TransferPy' in os.listdir():
			with open(f'{vidName}.TransferPy', 'wb') as r:
				pass


	async with aiohttp.ClientSession() as request:

		videoData = await request.get(url)
		
		Status = videoData.status
		ChunckSize = int(videoData.headers['Content-Length'])
		Encoding_File = videoData.headers['Content-Encoding']
		ChunckSizeMb = round(int(ChunckSize)/1000000)
		_FileMakedSwitch = False

		print('{} Bytes -> {} Mb\nArquivo -> {}.mp4\nbaixando...'.format(ChunckSize, ChunckSizeMb, vidName), end='\n\n')

		if Status == 200:

			FirstChunck = 0
			SecondChunck = 14999999
			_switch = True
			
			while _switch:

				header = {
					'accept-encoding': 'identity;q=1, *;q=0',
					'range': f'bytes={FirstChunck}-{SecondChunck}'

				}


				file = await request.get(url, headers=header)

				if file.status == 416:
					FirstChunck = ChunckSize - FirstChunck 
					SecondChunck = ChunckSize
					_switch = False

				else:
					file = await file.content.read() 

					await asyncio.sleep(0)

					while True:
						try:
							if f'{vidName}.TransferPy' in os.listdir() or _FileMakedSwitch == False:
								with open(f'{vidName}.TransferPy', 'ab') as r:
									r.write(file)

								FirstChunck += 15000000
								SecondChunck += 15000000

								if _FileMakedSwitch == False:
									_FileMakedSwitch = True
								
								break
							
							else:
								print(f'o arquivo "{vidName}.TransferPy" foi excluído.')
								return {"Fail": {'File': f'O arquivo "{vidName}.TransferPy" não existe.', 'ID-code': 0}} 

						except PermissionError:
							print('arquivo sendo usado, tentando novamente em alguns segundos...')
							time.sleep(10)

			os.rename(f'{vidName}.TransferPy', f'{vidName}.mp4')

			print(f'{vidName} terminou de baixar.')

			return {"Sucessful": {'B-size': ChunckSize, 'MB-size': ChunckSizeMb, 'Vid-name': f'{vidName}.mp4', 'ID-code': 1}}

		else:
			return {"Fail": {'code-status': Status, 'ID-code': 0}}


async def main(url, vidName):
	
	tasks = []
	subprocess.run(f'wmic process where processid="{os.getpid()}" CALL setpriority "64"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	for i in zip(url, vidName):
		tasks.append(asyncio.create_task(_Downloader(i[0], i[1])))

	runner = await asyncio.gather(*tasks)




def _LockDelAtExit() -> None:
	try:
		os.remove('.lock')
	
	except FileNotFoundError:
		pass

if __name__ == "__main__":

	if '.lock' not in os.listdir():

		with open('.lock', 'w') as r:		
			atexit.register(_LockDelAtExit)

			simdownload = ["https://fy.v.vrv.co/evs/5fa96b8cee0d2417a80fc90fa2577293/assets/1c2ed0f51c1885c352ec944f1ced44f6_4585910.mp4?Expires=1658340523\u0026Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9meS52LnZydi5jby9ldnMvNWZhOTZiOGNlZTBkMjQxN2E4MGZjOTBmYTI1NzcyOTMvYXNzZXRzLzFjMmVkMGY1MWMxODg1YzM1MmVjOTQ0ZjFjZWQ0NGY2XzQ1ODU5MTAubXA0IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjU4MzQwNTIzfX19XX0=\u0026Signature=mooQV0HqNAaiaPNd+D05DF/jMQGB6HVEmnnh8xO0x74=\u0026Key-Pair-Id=APKAJMWSQ5S7ZB3MF5VA",
						   'https://fy.v.vrv.co/evs/f37d7308be5ce07a2f6304a8468cc621/assets/5fe866d9c12b6a9a7dcee66335fa1826_4581996.mp4?Expires=1658336558&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9meS52LnZydi5jby9ldnMvZjM3ZDczMDhiZTVjZTA3YTJmNjMwNGE4NDY4Y2M2MjEvYXNzZXRzLzVmZTg2NmQ5YzEyYjZhOWE3ZGNlZTY2MzM1ZmExODI2XzQ1ODE5OTYubXA0IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjU4MzM2NTU4fX19XX0=&Signature=Em9I4oIXA3Ve8mdW+P60rrsHsaj+bS/t4LwlEntm2YM=&Key-Pair-Id=APKAJMWSQ5S7ZB3MF5VA']

			vidName = ['sd', 'fullhd']

			asyncio.run(main(simdownload, vidName))
			print('Todos os downloads foram finalizados.')

			time.sleep(3)		

	else:
		print('outra instância está sendo executada.')
		time.sleep(10)