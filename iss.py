#!/usr/bin/env python

__author__ = 'Ken Stephens'


import time
import turtle
import requests



iss_icon = 'iss_.gif'
world_map = 'map.gif'
base_url = 'http://api.open-notify.org'

def get_astronaut_info():
    "gets astronauts names who are in space and includes names of spacecraft"
    r = requests.get(base_url + '/astros.json')
    r.raise_for_status()
    return r.json()['people']


def locate_iss_spacestation():

    r = requests.get(base_url + '/iss-now.json')
    r.raise_for_status()
    position = r.json()['iss_position']


    r.raise_for_status()
    position = r.json()['iss_position']
    lat = float(position['latitude'])
    lon = float(position['longitude'])
    return lat, lon

def map_iss(lat, lon):

    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_icon)
    iss = turtle.Turtle()
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    return screen


def compute_rise_time(lat, lon):

    params = {'lat': lat, 'lon': lon}
    r = requests.get(base_url + '/iss-pass.json', params=params)
    r.raise_for_status()

    passover_time = r.json() ['response'] [1] ['risetime']
    return time.ctime(passover_time)



def main():
    astro_dict = get_astronaut_info()
    print('Current astronauts in spane: {}'.format(len(astro_dict)))
    for a in astro_dict:
        print(' - {} in {}'.format(a['name'], a['craft']))

    
    
    lat, lon = locate_iss_spacestation()
    print('Current ISS coordinates: lat={:.02f} lon={:.02f}'.format(lat, lon))

        
    


    screen = None
    try:
        screen = map_iss(lat, lon)


        indy_lat = 39.768403
        indy_lon = -86.158068
        location = turtle.Turtle()
        location.penup()
        location.color('yellow')
        location.goto(indy_lon, indy_lat)
        location.dot(5)
        location.hideturtle()
        next_pass = compute_rise_time(indy_lat, indy_lon)
        location.write(next_pass, align='center', font=('Arial', 12, 'normal'))
    except RuntimeError as e:
        print('ERROR: problem loading graphics: ' + str(e))
    
    if screen is not None:
        print('Click on screen to exit...')
        screen.exitonclick()


if __name__ == '__main__':
    main()
