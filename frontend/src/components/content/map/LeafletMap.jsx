import React from "react";
import * as Style from "./style";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useSelector } from "react-redux";
import { compose } from "react-recompose";
import withError from "../../../hoc/withHandleError";
import withLoading from "../../../hoc/withHandleLoading";

const LeafletMap = (props) => {
  const mapSettings = useSelector((state) => state.map.settings);

  return (
    <Style.LeafletMapWrapper>
      <MapContainer
        style={{ height: "100%" }}
        center={mapSettings.center}
        zoom={mapSettings.zoom}
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
