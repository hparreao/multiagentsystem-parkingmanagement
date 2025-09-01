import React from 'react'
import { createNativeStackNavigator } from '@react-navigation/native-stack'

import { InitialMap } from '../screens/InitialMap';
import { SelectSpot } from '../screens/SelectSpot';
import { ConfirmSpot } from '../screens/ConfirmSpot';
import { Directions } from '../screens/Directions';
import { Arrived } from '../screens/Arrived';

const { Navigator, Screen } = createNativeStackNavigator();

export function AppRoutes() {
    return (
        <Navigator screenOptions={{headerShown: false}}>
            <Screen name="initialmap"
            component={InitialMap}/>
            <Screen name="selectspot"
            component={SelectSpot}/>
            <Screen name="confirmspot"
            component={ConfirmSpot}/>
            <Screen name="directions"
            component={Directions}/>
            <Screen name="arrived"
            component={Arrived}/>
        </Navigator>
    );
}
