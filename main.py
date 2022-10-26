import discord
import os
import googlemaps
from midpoint import midPoint
from collegeCodes import codes
#Google stuff
API_KEY = os.environ['API_Key']
gmaps = googlemaps.Client(key = API_KEY)

#ChIJYU4kf3nAQIYR5nxwybBLcdY - baker college
place_id = "ChIJYU4kf3nAQIYR5nxwybBLcdY"
# Geocoding an address
def position(id):
#Returns a string for lan and lng from place_id
  geocode_result = gmaps.reverse_geocode(id)
  geocode_result = str(geocode_result[0]['geometry']['location']['lat'])+','+str(geocode_result[0]['geometry']['location']['lng'])
  return geocode_result

def distance(id1, id2):
  #returns distance
  distance = gmaps.distance_matrix("place_id:"+id1, "place_id:"+id2)
  return(distance['rows'][0]['elements'][0]['distance']['value'])

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

state = 0
college1 = ''
user1 = ''
user2 = ''
college2 = ''
@client.event
async def on_message(message):
    global state
    global college1
    global college2
    global user1
    global user2
    if message.author == client.user:
        return
    if message.content.startswith('$food'):
        place_results = gmaps.places_nearby(
          location = position(place_id),
          radius = 1000,
          type = 'cafe'
        )
        for place in place_results['results']:
          my_place_id = place['place_id']

          my_fields = ['name', 'type']
          place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
          print(place_details)
          await message.channel.send("There is a "+place_details['result']['name'])

    if message.content.startswith('$meetup'):
        channel = message.channel
        await channel.send('What is your college?')

        def check(m):
            global college1
            global college2
            if m.content.lower() in codes().keys():
              if state ==0:
                college1 = m.content.lower().title()
              else:
                college2 = m.content.lower().title()
            return m.content.lower() in codes().keys() and m.channel == channel

        msg = await client.wait_for('message', check=check)
        if state == 0:
          user1 = '{0.author.mention}'.format(msg)
          await channel.send('There is currently no one else looking for a meetup, please wait.'.format(msg))
          state = 1
        else:
          await channel.send('{0.author.mention} from '.format(msg)+college2+' and '+user1+' from '+college1+' are both looking for a meetup!')
          state = 0;

          #distance stuff
          college_id_1 = codes()[college1.lower()]
          college_id_2 = codes()[college2.lower()]
          mid = midPoint(position(college_id_1),position(college_id_2))
          college1_results = gmaps.places_nearby(
            location = mid,
            radius = 500,
            type = 'point_of_interest',
            open_now = True
            )
          if len(college1_results['results'])==0:
            college1_results = gmaps.places_nearby(
              location = mid,
              radius = 1000,
              type = 'point_of_interest',
              open_now = True
              )
          await message.channel.send('The following meetup spots are nearby')
          total = 0
          for place in college1_results['results']:
              my_place_id = place['place_id']
              my_fields = ['name', 'type']
              place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
              print(place_details)
              await message.channel.send(place_details['result']['name']+', which is '+str(distance(college_id_1,my_place_id))+' meters from '+college1+' and '+str(distance(college_id_2,my_place_id))+' meters from '+college2+'.')
              total +=1
              if total>5:
                break


client.run(os.environ['TOKEN'])
