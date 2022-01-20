from binance.spot import Spot
import pandas as pd

client = Spot()
print(client.time())

api_key = '6rQOJtUFhkMGICHob2zFZGPAa4CR0XNE1M2SiCt1Ri6OnpBYTjEKdJjnNDX9RK7n'
api_secret = 'QLlaZPkKK7kE8xGkLECSBUPgBG55EWJggAKSBOPisZEtu45DQrn43X3dGzT6F134'
client = Spot(key=api_key, secret=api_secret)



# Get account information
account = client.account()


df = pd.DataFrame(columns = ['asset','free','locked'])

for i in account['balances']:
    df = df.append(i,ignore_index=True)
df['free'] = df['free'].astype(float)
df = df[df.free != 0.0000]
print(df)