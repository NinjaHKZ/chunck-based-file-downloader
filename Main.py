import aiohttp, asyncio, json, os, time



async def Downloader(url, vidName) -> dict:

	async with aiohttp.ClientSession() as request:

		videoData = await request.get(url)
		
		Status = videoData.status
		ChunckSize = int(videoData.headers['Content-Length'])
		Encoding_File = videoData.headers['Content-Encoding']
		ChunckSizeMb = round(int(ChunckSize)/1000000)
		print('{} Bytes -> {} Mb'.format(ChunckSize, ChunckSizeMb), end='\n\n')
		print(Status)

		if Status == 200:

			FirstChunck = 0
			SecondChunck = 3999999
			_switch = True
			
			print('baixando...')
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
					while True:
						try:
							with open(f'{vidName}.mp4', 'ab') as r:
								r.write(file)

							FirstChunck += 4000000
							SecondChunck += 4000000

							break
						
						except PermissionError:
							print('arquivo sendo usado, tentando novamente em alguns segundos...')
							time.sleep(10)


			print('finish')

			return {"Sucessful": {'B-size': ChunckSize, 'MB-size': ChunckSizeMb}}




		else:
			return {"Fail": {'code-status': Status}}





async def main(url, vidName):
	tasks = []

	for i in zip(url, vidName):
		tasks.append(asyncio.create_task(Downloader(i[0], i[1])))

	runner = await asyncio.gather(*tasks)







simdownload = ["https://fy.v.vrv.co/evs/5fa96b8cee0d2417a80fc90fa2577293/assets/1c2ed0f51c1885c352ec944f1ced44f6_4585910.mp4?Expires=1658340523\u0026Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9meS52LnZydi5jby9ldnMvNWZhOTZiOGNlZTBkMjQxN2E4MGZjOTBmYTI1NzcyOTMvYXNzZXRzLzFjMmVkMGY1MWMxODg1YzM1MmVjOTQ0ZjFjZWQ0NGY2XzQ1ODU5MTAubXA0IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjU4MzQwNTIzfX19XX0=\u0026Signature=mooQV0HqNAaiaPNd+D05DF/jMQGB6HVEmnnh8xO0x74=\u0026Key-Pair-Id=APKAJMWSQ5S7ZB3MF5VA",
			   'https://fy.v.vrv.co/evs/f37d7308be5ce07a2f6304a8468cc621/assets/5fe866d9c12b6a9a7dcee66335fa1826_4581996.mp4?Expires=1658336558&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9meS52LnZydi5jby9ldnMvZjM3ZDczMDhiZTVjZTA3YTJmNjMwNGE4NDY4Y2M2MjEvYXNzZXRzLzVmZTg2NmQ5YzEyYjZhOWE3ZGNlZTY2MzM1ZmExODI2XzQ1ODE5OTYubXA0IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjU4MzM2NTU4fX19XX0=&Signature=Em9I4oIXA3Ve8mdW+P60rrsHsaj+bS/t4LwlEntm2YM=&Key-Pair-Id=APKAJMWSQ5S7ZB3MF5VA']

vidName = ['sd', 'fullhd']

asyncio.run(main(simdownload, vidName))
