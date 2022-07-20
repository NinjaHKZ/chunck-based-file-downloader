import os, aiohttp, asyncio
import time


async def download():
	size = 1439985348 # tamanho do video/arquivo
	first_range = 0
	last_range = 2999999 # deve conter -1 no valor final, exemplo: 10 -> 9, 1024 -> 1023

	async with aiohttp.ClientSession() as request:

		for i in range(80):
			header = {
				'accept-encoding': 'identity;q=1, *;q=0',
				'range': f'bytes={first_range}-{last_range}'
			}

			file = await request.get('https://fy.v.vrv.co/evs/5fa96b8cee0d2417a80fc90fa2577293/assets/1c2ed0f51c1885c352ec944f1ced44f6_4585910.mp4?Expires=1658340523\u0026Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9meS52LnZydi5jby9ldnMvNWZhOTZiOGNlZTBkMjQxN2E4MGZjOTBmYTI1NzcyOTMvYXNzZXRzLzFjMmVkMGY1MWMxODg1YzM1MmVjOTQ0ZjFjZWQ0NGY2XzQ1ODU5MTAubXA0IiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNjU4MzQwNTIzfX19XX0=\u0026Signature=mooQV0HqNAaiaPNd+D05DF/jMQGB6HVEmnnh8xO0x74=\u0026Key-Pair-Id=APKAJMWSQ5S7ZB3MF5VA"}},"__N_SSG":true},"page":"/[download]","query":{"download":"79c01a11a0d753d266db2d74c763155d:7ec687094514461abb0809c9b90d4ea76ca9beb0ab7649a1476f48877d1958c4711a29e87a321b5f45b2ba3ac0723ad65868911e47e42aadcdedde623915171b2b3a3c184cc5a018b2be5d070df81dd992dc6140cb8a487382e31ef42bed4f0dcff7d007edcf92a9bc0f152d249c8fd4e06aa05122f56471943b61592a4895f2a9a1049ff1c2647084e3c49a0f3a4677ebb5b91e3fa57e39c703f31cd898a6784c35a3718c20931e66eeafeb9c326a5a9003d777fae81900dfd989562dc4124a944ea92667886c58f9ce4e8290c9ff7b73f262ffe88684269feec9d30b57213b4563b589d18d2aeee876bf8909801038f5a49e979a085ca8b1527fb56a53730c7b0607c507929b1d2a60715593e80784a0165b00ac9d70ee30e7f2173d1a05db1b30b4619694f0edf2e0af2dc308276376a61a8619a2267b9d926057ce1643ce93318d52c809049d2ce0ce14b4672abb08e16059f810ce7fc2169322618c47accee1361867df6bd4449dd56b8061e8b3ffc1dd3f1e70a8bf83ab04d8b5d8fb2264b3cd66cbc914fceafa8b9cf7aa09081474286d2f8743c8c24f958232e083acd70b0b949be7bac62dc705c05c3c39f706b5e4a5ae56d409502924b5ce276471ccacf6ff8745cfa548b3867f3bdfabc7310fdb3a313693eae65a934176a13c0144128e7641d59ce9d9c8cc0303f28a9c28f199b623f863c14330d1a4c8e58157b7cf5c07a05186c7fb98c3b9a30fcde5cad5f089e5be2cdcc5d33b59f5096f20298a133b98e4c34e1f5812ed612c0e655f236f049f66361638cf966467ceb888"},"buildId":"yxR03voqUkScFxkTxQsk2', headers=header)
			
			file = await file.content.read()
			print('finalizado')

			with open(f'0.mp4', 'ab') as r:
				r.write(file)

			time.sleep(0.3)

			first_range += 3000000
			last_range += 3000000

loop = asyncio.get_event_loop()

loop.run_until_complete(download())