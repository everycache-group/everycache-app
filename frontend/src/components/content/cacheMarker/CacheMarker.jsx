import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

const CacheMarker = ({ position, title, ...props }) => {
  return (
    <Marker position={position} riseOnHover={true} zIndexOffset={10} {...props}>
      <Popup>
        <p>{title}</p>
      </Popup>
    </Marker>
  );
};

export default CacheMarker;
