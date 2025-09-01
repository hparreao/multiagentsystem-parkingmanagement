import { useRoute } from '@react-navigation/native';
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { ButtonGroup } from '@rneui/themed';
import { styles } from '../styles/styles';
import axios from 'axios';
import { LoadingComponent } from '../components/LoadingComponent';
import config from '../../config.json'

const url = `http://${config.ip_adress}:8000`

enum Price {
  Low = '$',
  Medium = '$$',
  High = '$$$'
}

interface PreferencesResponse {
  Environments: string[]
  Pricing: string[]
}

export function SelectSpot(props){
  const route = useRoute();
  const { item } = route.params
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndexEnv, setSelectedIndexEnv] = useState(0);
  const [selectedIndexPrice, setSelectedIndexPrice] = useState(0);
  const [buttonsEnv, setButtonsEnv] = useState<string[]>([]);
  const [buttonsPrice, setButtonsPrice] = useState<Price[]>([]);

  useEffect(() => {
    setIsLoading(true);
    axios.get<PreferencesResponse>(`${url}/parking_preferences`)
      .then(response => {
        const preferences: PreferencesResponse = response.data;
        setButtonsEnv(preferences.Environments)
        const price = preferences.Pricing.map(item => {
          if (item in Price) {
            return Price[item as keyof typeof Price];
          }
        }).filter(Boolean) as Price[]; // Filter out undefined values
        setButtonsPrice(price)
      })
      .catch(error => {
        console.error('Error fetching parking preferences:', error);
        Alert.alert('Error', 'Failed to fetch parking preferences. Please check your connection.');
      }).finally(() => {
        setIsLoading(false)
      });
}, []);
  
  const handleContinue = () => {
    setIsLoading(true);

    const pricing = getKeyFromValue(Price, buttonsPrice[selectedIndexPrice]);
    if (!pricing) {
      Alert.alert('Error', 'Please select a valid pricing option.');
      setIsLoading(false);
      return;
    }
    
    // d1 to be replaced with drivers id
    axios.get(`${url}/driver/d1?lat=${item.latitude}&lon=${item.longitude}&environment=${buttonsEnv[selectedIndexEnv]}&pricing=${pricing}`)
    .then(response => {
      if (response.data && response.data.Error) {
        Alert.alert('No Spot Available', 'No parking spots available matching your criteria. Please try different preferences.');
      } else {
        props.navigation.navigate('confirmspot', response.data)
      }
    })
    .catch(error => {
      console.error('Error requesting parking spot:', error);
      Alert.alert('Error', 'Failed to request parking spot. Please check your connection and try again.');
    }).finally(() => {
      setIsLoading(false)
    });
  }

  function getKeyFromValue(enumObj: any, value: string) {
    for (const key in enumObj) {
      if (enumObj[key] === value) {
        return key;
      }
    }
    return null;
  }

  return (
    <View style={styles.selectSpotWrapper}>
      {isLoading && <LoadingComponent />}
      <View>
        <View style={styles.selectSpotTitle}>
          <Text style={{fontSize: 20}}>Parking: {item.id.toUpperCase()}</Text>
          <Text>ISEP Parking </Text>
        </View>

        <Text style={{fontSize: 20}}>Price</Text>
        <ButtonGroup
        selectedIndex={selectedIndexPrice}
        buttons={buttonsPrice}
        onPress={(value) => {
          setSelectedIndexPrice(value);
        }}
        containerStyle={{ marginBottom: 80 }} />

        <Text style={{fontSize: 20}}>Environment</Text>
        <ButtonGroup
        selectedIndex={selectedIndexEnv}
        buttons={buttonsEnv}
        vertical
        onPress={(value) => {
          setSelectedIndexEnv(value);
        }} />
      </View>
      <Button title="Find Spot" onPress={handleContinue} />
    </View>
  );
};