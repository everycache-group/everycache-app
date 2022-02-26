import * as Style from "./style";
import React, { useState } from "react";
import Rating from "@mui/material/Rating";
import Box from "@mui/material/Box";
import StarIcon from "@mui/icons-material/Star";
import Popup from "../../shared/interaction/Popup/Popup";
import LeafletMap from "../map/LeafletMap";
import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import SettingsMapTracker from "./../map/SettingsMapTracker";
import CacheMarker from "./../cacheMarker/CacheMarker";
import { useSelector } from "react-redux";

const labels = {
  0.5: "Useless",
  1: "Useless+",
  1.5: "Poor",
  2: "Poor+",
  2.5: "Ok",
  3: "Ok+",
  3.5: "Good",
  4: "Good+",
  4.5: "Excellent",
  5: "Excellent+",
};

function RatingCommentCache({ ButtonName }) {
  const { name, lon, lat, description } = Cache;
  const [showMarker, setShowMarker] = useState(!!(lon && lat));

  const [value, setValue] = useState(2);
  const [hover, setHover] = useState(-1);
  const [trigger, setTrigger] = useState(true);
  const [loading, setLoading] = useState(false);

  const { zoom, center } = useSelector((state) => state.map.settings);

  return (
    <Popup trigger={trigger} setTrigger={setTrigger}>
      <Style.CacheFormWrapper>
        <Style.CacheFormContent>
          <Style.CacheInputWrapper>
            {" "}
            <Style.RatingWrapper>
              <Box
                sx={{
                  width: 200,
                  display: "flex",
                  alignItems: "center",
                }}
              >
                <Rating
                  name="hover-feedback"
                  value={value}
                  precision={0.5}
                  onChange={(event, newValue) => {
                    setValue(newValue);
                  }}
                  onChangeActive={(event, newHover) => {
                    setHover(newHover);
                    console.log("active change");
                  }}
                  emptyIcon={
                    <StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />
                  }
                />
                {value !== null && (
                  <Box sx={{ ml: 2 }}>
                    {labels[hover !== -1 ? hover : value]}
                  </Box>
                )}
              </Box>
            </Style.RatingWrapper>
          </Style.CacheInputWrapper>

          <LoadingButton
            sx={{ width: 120 }}
            onClick={() => {}}
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
          {showMarker && (
            <CacheMarker
              position={[1, 1]}
              draggable={true}
              eventHandlers={{
                dragend: (e) => {
                  const position = e.target.getLatLon();
                },
              }}
            />
          )}
          <SettingsMapTracker zoom={zoom} center={center} />
        </LeafletMap>
      </Style.CacheFormWrapper>
    </Popup>
  );
}

export default RatingCommentCache;
