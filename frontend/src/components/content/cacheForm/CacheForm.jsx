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
import { prepareErrors } from "../../../services/errorMessagesService"

function CacheForm({ Cache, OnFormSubmit, ButtonName }) {
  const { zoom, center } = useSelector((state) => state.map.settings);
  const { name, lon, lat, description } = Cache;
  const [showMarker, setShowMarker] = useState(!!(lon && lat));
  const [loading, setLoading] = useState(false);

  const handleLocationClick = (e) => {
    setFormValues({ ...formValues, lon: center[1], lat: center[0] });
    setShowMarker(true);
  };

  const {
    handleFormSubmit,
    handleUserInput,
    formValues,
    errors,
    setErrors,
    setFormValues,
  } = useForm(
    {
      name: name ? name : "",
      description: description ? description : "",
      lon,
      lat,
    },
    () => {
      if (OnFormSubmit instanceof Function) {
        OnFormSubmit(formValues, setErrors);
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
            helperText={prepareErrors(errors.name)}
            placeholder="Enter Cache Name Here..."
            value={formValues.name}
          />
          <Style.CacheCoordsWrapper>
            <TextField
              label="Longitude"
              type="number"
              size="small"
              id="lon"
              name="lon"
              error={!!errors.lon}
              helperText={prepareErrors(errors.lon)}
              onChange={handleUserInput}
              value={formValues.lon}
            />
            <TextField
              label="Latitude"
              type="number"
              size="small"
              id="lat"
              name="lat"
              error={!!errors.lat}
              helperText={prepareErrors(errors.lat)}
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
            helperText={prepareErrors(errors.description)}
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
          type="submit"
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
            position={[formValues.lat || 0, formValues.lon || 0]}
            draggable={true}
            eventHandlers={{
              dragend: (e) => {
                const position = e.target.getLatLng();
                setFormValues({
                  ...formValues,
                  lon: position.lon,
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
