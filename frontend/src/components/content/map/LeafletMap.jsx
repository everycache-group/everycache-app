import React, { useState, useEffect } from "react";
import * as Style from "./style";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useSelector } from "react-redux";
import { compose } from "react-recompose";
import withError from "../../../hoc/withHandleError";
import withLoading from "../../../hoc/withHandleLoading";

const LeafletMap = (props) => {
  const [map, setMap] = useState(null);

  const mapSettings = useSelector((state) => state.map.settings);
  const selectedCache = useSelector((state) => state.cache.selectedCache);

  //jump to selected cache on map
  useEffect(() => {
    if (map && selectedCache) {
      const { lat, lon } = selectedCache;
      map.flyTo({ lat, lon });
    }
  }, [selectedCache]);

  return (
    <Style.LeafletMapWrapper width={props.width}>
      <MapContainer
        style={{ height: "100%", borderRadius: 20 }}
        center={mapSettings.center}
        zoom={mapSettings.zoom}
        whenCreated={(map) => setMap(map)}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {props.children}
      </MapContainer>
    </Style.LeafletMapWrapper>
  );
};

export default compose(withError, withLoading)(LeafletMap);
