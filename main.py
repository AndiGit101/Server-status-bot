
from discord.ext import commands as cmd
from datetime import timedelta as dt
import requests as rq
import discord
import json
import time



#app start time
start = time.time()


#read  the current bot token
def get_token():
       
       token = ""
       
       with open("token.txt" ,"r+") as tok:
              
              token = tok.read()
  
       return token
   
             
#read current bot prefix if it has been updated or not
def read_prefix()->str:

       prefix = ""
       with open("current_prefix.txt" , "r+") as pf:

              prefix = pf.read()
              

       return prefix



intents = discord.Intents.default()
intents.message_content = True

#setup the client
client =  cmd.Bot(command_prefix=str(read_prefix()) , intents= intents)

              
                 
                     
                     
                     
                     
#Client command to give discord bot information                              
@client.command()
async def about(ctx) -> str:
         

            embed_help  = discord.Embed(color = 0x00df00)
            #  embed_help.thumbnail = "white-black-solidarity-handshake-stop-racism-pop-vector-8407995.jpg"
            embed_help.title = "AmIOnline"
            embed_help.set_author(name = 'Ad  ' , icon_url="https://s3.amazonaws.com/rsportz-production/people/avatars/000/286/172/large/avatar.png")
            embed_help.set_thumbnail(url = "https://vectorified.com/images/server-icon-minecraft-maker-2.png")
            embed_help.description = "AmIOnline is a bot that gives information on minecraft servers statuses in the network along with other tools.Use the command " + "**-general_help**" + " to get started!"
            await ctx.send(embed=embed_help)
      
#Client command to ping the discord bot
@client.command()
async def ping(ctx):
       
       
       await ctx.send(f"Pong!Responded in {client.latency*1000 :2f} ms ")
       

       
       
       




#client command to get the current server bot prefix
@client.command()
async def prefix(ctx):

       await ctx.send("Bot prefix--> **" + read_prefix() + "**")
       
       

       

#client command to set a new server prefix to the bot
@client.command()
async def prefix_set(ctx , prx):

       #write new prefix to file so nect time bot runs itll be updated
       with open("current_prefix.txt" , "w+") as change_prx:

              change_prx.write(prx)

       client.command_prefix = prx


       await ctx.send("Bot prefix has been changed for this server")

    



#client command to get the help commands for the bot 
@client.command()
async def general_help(ctx):
      
      
            embed_help  = discord.Embed(color = 0x009f00)
            #  embed_help.thumbnail = "white-black-solidarity-handshake-stop-racism-pop-vector-8407995.jpg"
            embed_help.title = "AmIOnline Help"
            embed_help.description = ":arrow_double_down:Command menu for AmIOnline:arrow_double_down:"
            embed_help.set_thumbnail(url = "https://vectorified.com/images/server-icon-minecraft-maker-2.png")
            embed_help.add_field(name = "help commands" , value = "``-prefix_set[prefix]``--> Change bot prefix for this server\n``-prefix``->Gets current bot prefix for this server" , inline= False)
            embed_help.add_field(name = "server commands", value = '``-status [server_address]``--> Gets the status of the minecraft server' ,inline= False)
            embed_help.add_field(name = "extra commands", value = "``-bot``-->Gives info on the bot\n``-ping``-->Pings bot" , inline= False)
            await ctx.send(embed=embed_help)

      
#client command to get the server status of a minecraft server
@client.command()
async def status(ctx , server_address) -> str:

    #fecth theb api request and return as a json
    fetch = rq.get("https://api.mcsrvstat.us/2/ " +  server_address)#api reuqest to get json data of the server

    json_data = open('dumped.json' , 'w')
    server_data = fetch.json() #just return json object


    #just dump data
    json_data.write((json.dumps(server_data)))#convert dict made to json and make a file

    valid_server = rq.get('https://api.mcsrvstat.us/debug/ping/' + server_address)
    

    #DEBUG
    server_request = valid_server.json()
    print(server_request)

    #make a list of bad request
    bad_request = ['No address to query' ,"Failed to connect or create a socket: 110 (Connection timed out)", f"Failed to connect or create a socket: 0 (php_network_getaddresses: getaddrinfo for {server_address} failed: Name or service not known)"]

    if not server_request in bad_request:            

        if server_data['online']:

                embed_online  = discord.Embed(color = 0x00ff00)
                embed_online.set_author(name = "Requested by "  + str(ctx.message.author) , icon_url= "https://s3.amazonaws.com/rsportz-production/people/avatars/000/286/172/large/avatar.png")
                embed_online.set_thumbnail(url ="https://api.mcsrvstat.us/icon/" + server_address)
                embed_online.title = "Server Status"
                embed_online.description = '**Online**' + f' :green_circle:'
                embed_online.add_field(name = "Server Info" , value = f"``\nPlayers online:``{server_data['players']['online']} / {server_data['players']['max']}``\n``Version:``{server_data['protocol_name']}``")
                await ctx.send(embed=embed_online)


        elif not server_data['online'] :

                embed_offline  = discord.Embed(color = 0xff0000)
                embed_offline 
                embed_offline.title = "Server Status"
                embed_offline.description = '**Offline**' + ' :red_circle:\nIt appears that this server is offline'
                await ctx.send(embed=embed_offline)

    else:
         
         await ctx.send("``Invalid server address, Please input a valid server adress(Ex: mc.hypixel.net for Hypixel)``")



#client command to get specific info on the bot
@client.command()
async def bot(ctx):
       
       #Get the bots uptime
       
       #When the bot command executes get the snapshot time to calc diff
       curr_time = time.time()
       

       
       embed = discord.Embed(color =0x00ff00 )
       
       embed.title = "Bot info"
       embed.description = "Information on AmIOnline"
       embed.add_field(name = "Library", value = "``discord.py(version 3.10)``")
       embed.add_field(name = "Bot latency", value  = f"``{client.latency*1000 :2f} ms``")
       embed.add_field(name = "Uptime", value = f"Uptime for AmIOnline:``{dt(seconds= int(curr_time - start))}``")
       
       await ctx.send(embed  = embed)
    
       
       


            

        
 
    
    




#Start the application on discord end
if __name__ == "__main__":

    print("Bot running")
    
    #This shows that the bot is runni
           
    client.run(get_token())#run  the bot
    
    



