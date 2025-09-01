import React, { useEffect, useState } from 'react';
import { Alert, View, Text } from 'react-native';
import MapView , { Marker, Polyline } from 'react-native-maps';
import Icon  from 'react-native-vector-icons/FontAwesome';
import { CoordProps, LocationCoordProps, MapProps } from '../types/types';
import { styles } from '../styles/styles';
import { PERMISSIONS, request } from 'react-native-permissions';
import Geolocation from '@react-native-community/geolocation';
import config from '../../config.json';


export function Map({ markers, polylineCoords }: MapProps) {
  const [currentLocation, setCurrentLocation] = useState<CoordProps | null>(null)
  const [coords, setCoords] = useState<Array<{ latitude: number, longitude: number }>>([]);
  const origin: LocationCoordProps = {
    id: 'P',
    latitude: 41.17880410608253, //currentLocation.latitude
    longitude: -8.609241948747831 //currentLocation.longitude
  }
  useEffect(() => {
    request(PERMISSIONS.ANDROID.ACCESS_FINE_LOCATION).then((result) => {
        if (result === 'granted') {
            Geolocation.getCurrentPosition(
                (position) => {
                    setCurrentLocation(position.coords);
                },
                (error) => {
                    Alert.alert("Erro", "Não foi possível obter a localização");
                },
                { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
            );
        } else {
            Alert.alert("Habilite a permissão para obter a localização");
        }
    });
}, []);

useEffect(()=> {
  if(polylineCoords){
    const apiUrl = `https://maps.googleapis.com/maps/api/directions/json?origin=${origin.latitude},${origin.longitude}&destination=${polylineCoords.latitude},${polylineCoords.longitude}&key=${config.api_key}`;
    
    fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      if (data.routes.length) {
        setCoords(decode(data.routes[0].overview_polyline.points)); // Decodifica os pontos do polyline
      }
    })
    .catch(e => {
      console.warn(e);
    });
  }

}, [polylineCoords])


  return (
        <View style={styles.container}>
          {

            currentLocation && <MapView style={styles.map}
            initialRegion={{
              //posição no mapa - to be replaced with current location
              latitude: markers[0].latitude, 
              longitude: markers[0].longitude,
              //latitude: currentLocation.latitude, 
              //longitude: currentLocation.longitude,
              // aproximação mostrada no mapa
              latitudeDelta: 0.002,
              longitudeDelta: 0.002
            }}
            >
            {
              <Marker identifier='origin' coordinate={{          
                latitude: origin.latitude, 
              longitude:  origin.longitude}
              }>
                <Icon name="car" size={28} color="green" />
              </Marker> }
              { markers.map((item: LocationCoordProps)=> (
                <Marker key={item.id} identifier={item.id} 
                  coordinate={{          
                  latitude: item.latitude, 
                  longitude: item.longitude
                }}>
                  <View style={styles.marker}>
                    <Text  style={styles.text} >
                    {item.id.toUpperCase()}
                    </Text>
                  </View>
                </Marker>
              ))
              }
            {coords && 
            <Polyline 
              coordinates={coords}
              strokeColor="#000" 
              strokeWidth={3}
            />}
            </MapView>
          }
        </View>
  );
}

function decode(t) {
  let points = []
  let index = 0, len = t.length;
  let lat = 0, lng = 0;
  while (index < len) {
    let b, shift = 0, result = 0;
    do {
      b = t.charAt(index++).charCodeAt(0) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
    lat += dlat;
    shift = 0;
    result = 0;
    do {
      b = t.charAt(index++).charCodeAt(0) - 63;
      result |= (b & 0x1f) << shift;
      shift += 5;
    } while (b >= 0x20);
    let dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
    lng += dlng;
    points.push({latitude: lat / 1e5, longitude: lng / 1e5});
  }
  return points;
}
