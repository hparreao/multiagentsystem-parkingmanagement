import { StyleSheet, Dimensions } from 'react-native';

export const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#fff',
      alignItems: 'center',
      justifyContent: 'center',
    },
    selectSpotWrapper: {
        flex: 1, 
        marginHorizontal: 10, 
        justifyContent: 'space-between'
    },
    selectSpotTitle: {
        marginVertical: 30,
        paddingBottom: 10, 
        borderBottomWidth: 1, 
        borderBottomColor: 'gray', 
        flex: 0, 
        gap: 30
    },
     map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
    marker: {
      width: 32,
      height: 32,
      backgroundColor: "transparent",
      borderColor: "blue",
      borderWidth: 2,
      borderStyle: 'solid',
      borderRadius: 50,
      justifyContent: 'center',
      alignItems: 'center'
    },
    text: {
      position: 'absolute',
      fontSize: 24,
      color: 'red',
      fontWeight: 'bold',
    },
    searchContainer: {
      position: 'absolute',
      zIndex: 1,
      width: '100%',
      bottom: 0,
      backgroundColor: 'white'
    },
    itemStyle: {
      padding: 10,
    },
    textInputStyle: {
      height: 40,
      borderWidth: 1,
      paddingLeft: 20,
      margin: 5,
      borderColor: '#009688',
      backgroundColor: '#FFFFFF',
    },
    selectedSpot: {
      flex: 1,
      gap: 10,
      alignItems: 'center'
    },
    loading: {
      ...StyleSheet.absoluteFillObject,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)', 
    }
  });