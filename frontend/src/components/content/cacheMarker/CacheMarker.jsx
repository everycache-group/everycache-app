import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";
import { useDispatch, useSelector } from "react-redux";
import { selectRow } from "../../../redux/slices/cacheSlice";
import { changeCenter } from "../../../redux/slices/mapSlice"

const CacheMarker = ({ position, title, cacheId, owner, ...props }) => {
  const dispatch = useDispatch();

  const selectedCache = useSelector((state) => state.cache.selectedCache);
  const currentUsername = useSelector((state) => state.user.username);
  const userRatings = useSelector((state) => state.user.ratings);
  const existingRating = userRatings.find(x => x.cache_id == cacheId);
  const visited = !!existingRating && existingRating.rating > 0;

  let icon = L.icon({
      iconUrl: "/icons/disabled_marker.svg",
      iconSize: [50, 115],
    });

  if (currentUsername == owner) {
    icon = L.icon({
      iconUrl: "/icons/user_marker.svg",
      iconSize: [50, 115],
    });
  }

  if (visited) {
    icon = L.icon({
      iconUrl: "/icons/visited_marker.svg",
      iconSize: [50, 115],
    });
  }

  if (selectedCache && selectedCache.id == cacheId) {
    icon = L.icon({
      iconUrl: "/icons/active_marker.svg",
      iconSize: [50, 115],
    });
  }

  if (selectedCache && selectedCache.id == cacheId && currentUsername == owner) {
    icon = L.icon({
      iconUrl: "/icons/active_user_marker.svg",
      iconSize: [50, 115],
    });
  }

  if (selectedCache && selectedCache.id == cacheId && visited) {
    icon = L.icon({
      iconUrl: "/icons/active_visited_marker.svg",
      iconSize: [50, 115],
    });
  }




  const onOpen = () => {
    dispatch(selectRow(cacheId));
  }

  return (
    <Marker
      position={position}
      icon={icon}
      riseOnHover={true}
      zIndexOffset={10}
      eventHandlers={{
        click: onOpen
      }}
      {...props}
    >
      <Popup>
        <p>{title}</p>
      </Popup>
    </Marker>
  );
};

export default CacheMarker;
