import { useState, useEffect } from "react";
import { useMapEvents } from "react-leaflet";
import { useDispatch } from "react-redux";
import { changeZoom, changeCenter } from "./../../../redux/slices/mapSlice";

function SettingsMapTracker(props) {
  const [zoom, setZoom] = useState(props.zoom);
  const [center, setCenter] = useState(props.center);

  const dispatch = useDispatch();

  const map = useMapEvents({
    zoomend: () => {
      setZoom(map.getZoom());
    },
    mouseup: (e) => {
      const { lat, lng } = map.getCenter();
      setCenter([lat, lng]);
    },
  });

  useEffect(() => {
    dispatch(changeZoom(zoom));
  }, [zoom]);

  useEffect(() => {
    dispatch(changeCenter(center));
  }, [center]);

  return null;
}

export default SettingsMapTracker;
