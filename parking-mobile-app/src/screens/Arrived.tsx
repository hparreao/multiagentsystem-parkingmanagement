import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';
import FontAwesome from 'react-native-vector-icons/FontAwesome';

import init from 'react_native_mqtt';
import AsyncStorage from '@react-native-async-storage/async-storage';
import config from '../../config.json'

export function Arrived() {
    const [parked, setParked] = useState(false);
    const [left, setLeft] = useState(false);
    const [price, setPrice] = useState(0);
    const [connectionStatus, setConnectionStatus] = useState('disconnected');

    init({
      size: 10000,
      storageBackend: AsyncStorage,
      defaultExpires: 1000 * 3600 * 24,
      enableCache: true,
      reconnect: true,
      sync: {},
    });

    function onConnect() {
      setConnectionStatus('connected');
      console.log("MQTT Connected");
      try {
        client.subscribe('parked', { qos: 0 });
        console.log("Subscribed to 'parked' topic");
      } catch (error) {
        console.error("Failed to subscribe:", error);
        Alert.alert('Subscription Error', 'Failed to subscribe to parking updates.');
      }
    }

    function onConnectionLost(responseObject) {
      setConnectionStatus('disconnected');
      if (responseObject.errorCode !== 0) {
        console.log("MQTT Connection Lost: " + responseObject.errorMessage);
        Alert.alert('Connection Error', 'Lost connection to the parking system.');
      }
    }

    function onMessageArrived(message) {
      console.log("MQTT Message Arrived: " + message.payloadString);
      try {
        const messageMqtt = message.payloadString.split(" ");
        const parkedStatus = messageMqtt[0];
        const priceValue = messageMqtt[1];
        
        if (parkedStatus === '1') {
          setParked(true);
        } else if (parkedStatus === '0') {
          setLeft(true);
          if (priceValue) {
            setPrice(parseFloat(priceValue) || 0);
          }
        }
      } catch (error) {
        console.error("Error processing MQTT message:", error);
      }
    }

    function onFailure(err) {
      setConnectionStatus('error');
      console.log('MQTT Connect failed!', err);
      Alert.alert('Connection Error', 'Failed to connect to the parking system. Please check your network connection.');
    }

    const client = new Paho.MQTT.Client(config.ip_adress, 9001, 'parked_client_' + Math.random().toString(36).substring(7));
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    useEffect(() => {
      try {
        client.connect({ 
          onSuccess: onConnect, 
          useSSL: false, 
          timeout: 30, 
          onFailure: onFailure 
        });
      } catch (error) {
        console.error("Failed to initialize MQTT connection:", error);
        Alert.alert('Connection Error', 'Failed to initialize connection to the parking system.');
      }

      // Cleanup function to disconnect when component unmounts
      return () => {
        if (client && client.isConnected()) {
          client.disconnect();
        }
      };
    }, []);

    return (
      <View style={styles.container}>
        {connectionStatus === 'error' && (
          <View style={styles.statusIndicator}>
            <Text style={styles.errorMessage}>Connection Error</Text>
          </View>
        )}
        
        {!parked && !left &&    
        <View>
            <FontAwesome style={styles.icon} name="check-circle" size={150} color="green" />
            <Text style={styles.message}>You've arrived!</Text>
            {connectionStatus === 'connecting' && <Text style={styles.status}>Connecting to parking system...</Text>}
        </View>
        }
        
        {parked && !left &&    
        <View>
            <FontAwesome name="car" size={150} color="green" />
            <Text style={styles.message}>Parked!</Text>
        </View>
        }
        
        {parked && left &&    
        <View>
            <FontAwesome style={styles.icon} name="check-circle" size={150} color="green" />
            <Text style={styles.message}>Finished!</Text>
            <Text style={styles.payed}>${price.toFixed(2)} Payment completed</Text>
        </View>
        }
      </View>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#ffffff',
  },
  icon: {
    textAlign: 'center'
  },
  message: {
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 30,
    textAlign: 'center'
  },
  payed: {
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: 30,
    textAlign: 'center'
  },
  statusIndicator: {
    position: 'absolute',
    top: 50,
    padding: 10,
    backgroundColor: '#ffebee',
    borderRadius: 5,
  },
  errorMessage: {
    color: '#c62828',
    fontWeight: 'bold',
  },
  status: {
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
    color: '#666',
  },
});