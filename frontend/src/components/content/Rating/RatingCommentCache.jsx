import * as Style from "./style";
import React, { useEffect, useState } from "react";
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
import { AddRating } from "../../../redux/slices/cacheSlice";
import { useDispatch } from "react-redux";
import { Typography } from "@mui/material";
import { useSnackbar } from "notistack";
import TextField from "@mui/material/TextField";

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

function RatingCommentCache({ OnActionClose }) {
  const { name, lng, lat, description } = Cache;
  const [showMarker, setShowMarker] = useState(!!(lng && lat));
  const [comment, setComment] = useState("");

  const dispatch = useDispatch();
  const snackBar = useSnackbar();

  const [rating, setRating] = useState(2);
  const [hover, setHover] = useState(-1);
  const [trigger, setTrigger] = useState(true);
  const [loading, setLoading] = useState(false);

  const currentCache = useSelector((state) => state.cache.selectedCache);

  const OnRatingChange = (event, newValue) => {
    dispatch(AddRating({ id: currentCache.id, rating: hover })).then(
      ({ meta }) => {
        if (meta.requestStatus === "fulfilled") {
          setRating(hover);
          snackBar.enqueueSnackbar("Cache Rated Succesfully!", {
            variant: "success",
          });
        }
      }
    );
  };

  const OnCommentChange = (e) => {
    setComment(e.target.value);
  };

  const OnCommentButtonClick = (e) => {};

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);

  const { zoom, center } = useSelector((state) => state.map.settings);

  return (
    <Popup trigger={trigger} setTrigger={setTrigger}>
      <Style.CacheFormWrapper>
        <Style.CacheFormContent>
          <Style.CacheInputWrapper>
            <Typography variant="h6"> Rate cache</Typography>
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
                  value={rating}
                  precision={0.5}
                  onChange={OnRatingChange}
                  onChangeActive={(event, newHover) => {
                    setHover(newHover);
                  }}
                  emptyIcon={
                    <StarIcon style={{ opacity: 0.55 }} fontSize="inherit" />
                  }
                />
              </Box>

              {rating !== null && (
                <Typography variant="h6">
                  {labels[hover !== -1 ? hover : rating]}
                </Typography>
              )}
            </Style.RatingWrapper>
            <TextField
              multiline
              placeholder="Enter Comment Here..."
              label="Comment"
              id="comment"
              onChange={OnCommentChange}
              name="comment"
              maxRows={10}
            />
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
            Add Comment
          </LoadingButton>
        </Style.CacheFormContent>
        <LeafletMap width={500}>
          {showMarker && (
            <CacheMarker
              position={[1, 1]}
              draggable={true}
              eventHandlers={{
                dragend: (e) => {
                  const position = e.target.getLatLng();
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
