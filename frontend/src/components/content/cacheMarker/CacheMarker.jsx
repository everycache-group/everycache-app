import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

const CacheMarker = ({ position, title, ...props }) => {
  const icon = L.icon({
    iconUrl: "/icons/active_marker.svg",
    iconSize: [50, 115],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
  });

  return (
    <Marker
      position={position}
      icon={icon}
      riseOnHover={true}
      zIndexOffset={10}
      {...props}
    >
      <Popup>
        <p>{title}</p>
      </Popup>
    </Marker>
  );
};

export default CacheMarker;
