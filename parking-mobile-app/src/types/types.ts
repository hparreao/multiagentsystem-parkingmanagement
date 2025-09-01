export type CoordProps = {
    latitude: number;
    longitude: number;
  }

export  type LocationCoordProps =  CoordProps & {
    id: string
  } 

  export type MapProps = {
    markers: LocationCoordProps[];
    polylineCoords?: LocationCoordProps;
  };