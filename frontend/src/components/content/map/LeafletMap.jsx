import React from "react";
import * as Style from "./style";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

const LeafletMap = () => {
  return (
    <Style.LeafletMapWrapper>
      <MapContainer
        style={{ height: "100%" }}
        center={[51.505, -0.09]}
        zoom={13}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker></Marker>
      </MapContainer>
    </Style.LeafletMapWrapper>
  );
};

export default LeafletMap;
