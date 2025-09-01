import React, { useRef, useMemo, useEffect } from 'react';
import { View, Text,  Button } from 'react-native';
import { BottomSheetModal, BottomSheetModalProvider } from '@gorhom/bottom-sheet';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { Map } from '../components/Map'
import { LocationCoordProps } from '../types/types';
import { useRoute } from '@react-navigation/native';
import { styles } from '../styles/styles';

export function ConfirmSpot(props) {
  const route = useRoute();
  const result = route.params;
  
  const bottomSheetModalRef = useRef(null);
  const snapPoints = useMemo(() => ["30%"], []);

  useEffect(()=> {
    bottomSheetModalRef.current.present();
  }, [])

  const handleConfirm = () => {
    props.navigation.navigate('directions', {markers})
  }

  const markers: LocationCoordProps[] = [{
      id: 'P',
      latitude: result.lat,
      longitude: result.lon
  }]

  return (
    <GestureHandlerRootView style={{flex: 1}}> 
      <BottomSheetModalProvider>
        <View style={styles.container}>
          <Map markers={markers} />
          <View style={styles.searchContainer}>
              <BottomSheetModal
                ref={bottomSheetModalRef}
                index={0}
                snapPoints={snapPoints}
                enablePanDownToClose={false}
              >
                <View style={styles.selectSpotWrapper}>
                  <View style={styles.selectedSpot}>
                    <Text style={{fontSize: 20}}>This will be your parking spot:</Text>
                    <Text>Hourly Cost: {result.pricing}</Text>
                    <Text>Environment: {result.environment}</Text>
                  </View>
                  <Button title="Confirm Spot" onPress={handleConfirm} />
                </View>
              </BottomSheetModal>
          </View>
        </View>
      </BottomSheetModalProvider>
    </GestureHandlerRootView>
  );
}