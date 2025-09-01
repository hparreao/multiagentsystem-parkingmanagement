import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { styles } from '../styles/styles';

export function LoadingComponent() {
  return (
    <View style={styles.loading}>
      <ActivityIndicator size="large" color="blue" />
    </View>
  );
};