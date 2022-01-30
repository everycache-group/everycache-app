import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

const CacheMarker = ({ position, title }) => {
  const iconMarker = L.icon({});

  return (
    <Marker
      draggable={false}
      position={position}
      riseOnHover={true}
      zIndexOffset={10}
    >
      <Popup>
        <p>{title}</p>
      </Popup>
    </Marker>
  );
};

export default CacheMarker;
