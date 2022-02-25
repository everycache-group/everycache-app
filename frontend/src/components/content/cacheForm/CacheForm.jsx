import React, { useEffect, useState } from "react";
import * as Style from "./style";
import LeafletMap from "../map/LeafletMap";
import useForm from "./../../../hooks/useForm";
import TextField from "@mui/material/TextField";
import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import { MdMyLocation } from "react-icons/md/";
import SettingsMapTracker from "./../map/SettingsMapTracker";
import CacheMarker from "./../cacheMarker/CacheMarker";
import { useSelector } from "react-redux";
import { fromRenderProps } from "react-recompose";

function CacheForm({ Cache, OnFormSubmit, ButtonName }) {
  const { zoom, center } = useSelector((state) => state.map.settings);
  const { name, lng, lat, description } = Cache;
  const [showMarker, setShowMarker] = useState(!!(lng && lat));
  const [loading, setLoading] = useState(false);

  const handleLocationClick = (e) => {
    setFormValues({ ...formValues, lng: center[1], lat: center[0] });
    setShowMarker(true);
  };

  const {
    handleFormSubmit,
    handleUserInput,
    formValues,
    errors,
    setFormValues,
  } = useForm(
    {
      name: name ? name : "",
      description: description ? description : "",
      lng,
      lat,
    },
    () => {
      if (OnFormSubmit instanceof Function) {
        OnFormSubmit(formValues);
      }
    }
  );

  return (
    <Style.CacheFormWrapper>
      <Style.CacheFormContent>
        <Style.CacheInputWrapper>
          <TextField
            id="name"
            label="Name"
            onChange={handleUserInput}
            name="name"
            error={!!errors.name}
            helperText={errors.name}
            placeholder="Enter Cache Name Here..."
            value={formValues.name}
          />
          <Style.CacheCoordsWrapper>
            <TextField
              label="Longitude"
              type="number"
              size="small"
              id="lng"
              name="lng"
              error={!!errors.lng}
              helperText={errors.lng}
              onChange={handleUserInput}
              value={formValues.lng}
            />
            <TextField
              label="Latitude"
              type="number"
              size="small"
              id="lat"
              name="lat"
              error={!!errors.lat}
              helperText={errors.lat}
              onChange={handleUserInput}
              value={formValues.lat}
            />
          </Style.CacheCoordsWrapper>
          <TextField
            multiline
            placeholder="Enter Cache Description Here..."
            label="Description"
            id="description"
            onChange={handleUserInput}
            name="description"
            error={!!errors.description}
            helperText={errors.description}
            maxRows={10}
            value={formValues.description}
          />
        </Style.CacheInputWrapper>

        <LoadingButton
          sx={{ width: 120 }}
          onClick={handleFormSubmit}
          endIcon={<SendIcon />}
          loadingPosition="end"
          loading={loading}
          variant="contained"
          color="success"
        >
          {ButtonName}
        </LoadingButton>
      </Style.CacheFormContent>
      <LeafletMap width={500}>
        <Style.MarkerLocationWrapper>
          <MdMyLocation
            onClick={handleLocationClick}
            size={22}
            style={{ lineHeight: 30, height: 30 }}
          />
        </Style.MarkerLocationWrapper>
        {showMarker && (
          <CacheMarker
            position={[formValues.lat, formValues.lng]}
            draggable={true}
            eventHandlers={{
              dragend: (e) => {
                const position = e.target.getLatLng();
                setFormValues({
                  ...formValues,
                  lng: position.lng,
                  lat: position.lat,
                });
              },
            }}
          />
        )}
        <SettingsMapTracker zoom={zoom} center={center} />
      </LeafletMap>
    </Style.CacheFormWrapper>
  );
}

export default CacheForm;
