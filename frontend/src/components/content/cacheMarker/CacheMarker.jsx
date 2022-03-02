import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";
import { useDispatch } from "react-redux";
import { selectRow } from "../../../redux/slices/cacheSlice";

const CacheMarker = ({ position, title, cacheId, ...props }) => {
  const dispatch = useDispatch();
  const icon = L.icon({
    iconUrl: "/icons/active_marker.svg",
    iconSize: [50, 115],
    iconAnchor: [22, 94],
    popupAnchor: [-3, -76],
  });

  const onOpen = () => {
    dispatch(selectRow(cacheId));
  }

  return (
    <Marker
      position={position}
      icon={icon}
      riseOnHover={true}
      zIndexOffset={10}
      {...props}
    >
      <Popup onOpen={onOpen}>
        <p>{title}</p>
      </Popup>
    </Marker>
  );
};

export default CacheMarker;
