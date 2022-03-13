import * as Style from "./style";
import React, { useState, useEffect } from "react";
import Rating from "@mui/material/Rating";
import Box from "@mui/material/Box";
import StarIcon from "@mui/icons-material/Star";
import Popup from "../../shared/interaction/Popup/Popup";
import LoadingButton from "@mui/lab/LoadingButton";
import SendIcon from "@mui/icons-material/Send";
import CacheMarker from "./../cacheMarker/CacheMarker";
import { useSelector, useDispatch } from "react-redux";
import { addRating, updateRating } from "../../../redux/slices/userSlice";
import { useSnackbar } from "notistack";
import { alertGenericErrors } from "../../../services/errorMessagesService"

const labels = {
  1: "Useless",
  2: "Poor",
  3: "Ok",
  4: "Good",
  5: "Excellent",
};

function RatingCommentCache({ OnActionClose, cacheId }) {
  const userRatings = useSelector((state) => state.user.ratings);
  const existingRating = userRatings.find(x => cacheId == x.cache_id);
  const snackBar = useSnackbar();
  const [value, setValue] = useState(existingRating?.rating || 3);
  const [hover, setHover] = useState(-1);
  const [trigger, setTrigger] = useState(true);
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();


  const onVisitSubmit = () => {
    if (existingRating){
      dispatch(updateRating({visit_id: existingRating.id, rating: value ?? 0}))
        .unwrap()
        .then(() => {
          snackBar.enqueueSnackbar("Cache Rating Updated Succesfully!", {
            variant: "success",
          });
          setTrigger(false);
          OnActionClose();
        })
        .catch((payload) => {
          alertGenericErrors(payload, snackBar);
        });
    }
    else{
      dispatch(addRating({cache_id: cacheId, rating: value ?? 0}))
        .unwrap()
        .then(() => {
          snackBar.enqueueSnackbar("Cache Rated Succesfully!", {
            variant: "success",
          });
          setTrigger(false);
          OnActionClose();
        })
        .catch((payload) => {
          alertGenericErrors(payload, snackBar);
        });
    }
  }

  useEffect(() => {
    if (trigger === false) {
      if (OnActionClose instanceof Function) {
        OnActionClose();
      }
    }
  }, [trigger]);


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
                  onChange={(event, newValue) => {
                    setValue(newValue);
                  }}
                  onChangeActive={(event, newHover) => {
                    setHover(newHover);
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
            onClick={onVisitSubmit}
            endIcon={<SendIcon />}
            loadingPosition="end"
            loading={loading}
            variant="contained"
            color="success"
            type="submit"
          >
            {(!!existingRating && existingRating.rating > 0) ? "Update rating" : "Mark as Visited"}
          </LoadingButton>
        </Style.CacheFormContent>
      </Style.CacheFormWrapper>
    </Popup>
  );
}

export default RatingCommentCache;
