import { useState, useEffect } from "react";
import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import CommentsDisabledIcon from '@mui/icons-material/CommentsDisabled';
import AddCommentIcon from '@mui/icons-material/AddComment';
import Typography from '@mui/material/Typography';
import * as Style from "./style.js"
import { useDispatch, useSelector } from "react-redux";
import { getComments } from "../../../redux/slices/commentSlice"
import Chip from '@mui/material/Chip';
import AddCommentPopup from "../CommentPopup/AddCommentPopup/AddCommentPopup"
import EditCommentPopup from "../CommentPopup/EditCommentPopup/EditCommentPopup"
import DeleteCommentPopup from "../CommentPopup/DeleteCommentPopup/DeleteCommentPopup"

export default function CommentList() {
  const [open, setOpen] = useState(false);
  const [action, setAction] = useState("");
  const [selectedComment, setSelectedComment] = useState(null);
  const [cacheId, setCacheId] = useState(null);
  const selectedCache = useSelector((state) => state.cache.selectedCache);
  const {id: currentUserId, role: currentUserRole} = useSelector((state) => state.user);
  const comments = useSelector((state) => state.comment.comments);
  const dispatch = useDispatch();


  const handleToggleOpen = () => {
    if (open) {
      setOpen(false);
    }
    else {
      setOpen(true);
      dispatch(getComments(selectedCache.id));
    }
  }

  useEffect(() => {
    if( selectedCache?.id != cacheId ){
        dispatch(getComments(selectedCache.id));
        setCacheId(selectedCache.id);
    }
  })

  const handleAddComment = () => {
    setAction("add");
  }

  const handleEditComment = (comment) => {
    setSelectedComment(comment);
    setAction("update");
  }

  const handleDeleteComment = (comment) => {
    setSelectedComment(comment);
    setAction("delete");
  }

  const onActionClose = () => {
    setAction("");
    setSelectedComment(null);
  }

  const dateOptions = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric' };

  return (
    <>
      <Style.CommentListWrapper>
        <Style.CommentListContent key={selectedCache?.id}>
        {open &&
          <List sx={{ width: '100%', bgcolor: 'background.paper', "overflowY": "auto", "overflowX": "clip", height: "85%" }}>
              {!comments.length &&
                <ListItemText key="comments-not-found"
                  primary={
                    <Typography
                      sx={{ "margin": "20px" }}
                      component="span"
                      variant="subtitle2"
                      color="text.primary"
                    >
                      No comments yet.
                    </Typography>
                  }
                />
              }
              {comments.map((comment, i) => {
                return <React.Fragment key={i}>
                  <Style.CommentListItem key={comment.id} alignItems="flex-start">
                    <ListItemText
                        style={{"wordWrap": "break-word", "maxWidth": "60%"}}
                      primary={
                        <Typography
                          sx={{ display: 'inline' }}
                          component="span"
                          variant="body1"
                          color="text.primary"
                        >
                          {comment.author.username}
                        </Typography>
                      }
                      secondary={
                        <React.Fragment>
                          <Typography
                            sx={{ display: 'inline' }}
                            component="span"
                            variant="caption"
                            color="text.primary"
                          >
                            {(new Date(comment.created_on)).toLocaleDateString("en-US", dateOptions)}
                          </Typography>
                          <br/>
                          <Typography
                            sx={{ display: 'inline' }}
                            component="span"
                            variant="subtitle2"
                            color="text.secondary"
                          >
                            {comment.text}
                          </Typography>
                        </React.Fragment>
                      }
                    />
                    <Typography
                      sx={{ display: 'inline' }}
                      component="span"
                      variant="subtitle2"
                      color="text.secondary"
                    >
                    {((comment.author.id == currentUserId) || (currentUserRole == "Admin")) && <>
                      <Chip label="Edit" size="small" variant="outlined" style={{"marginRight": "3px"}} onClick={() => handleEditComment(comment)}/>
                      <Chip label="Delete" size="small" variant="outlined" onClick={() => handleDeleteComment(comment)}/>
                    </>}
                    </Typography>
                  </Style.CommentListItem>
                  {i < (comments.length - 1) && <Divider key={`divider{comment.id}`} variant="inset" component="li" />}
                </React.Fragment>
              })}
          </List>
        }
          {selectedCache && <Style.CommentMenuWrapper>

            <Style.CommentIconAvatar style={{visibility: !open && "hidden"}} onClick={handleAddComment}>
              <AddCommentIcon />
            </Style.CommentIconAvatar>
            <Style.CommentIconAvatar onClick={handleToggleOpen}>
              {!open &&<Style.ListCommentIcon/>}
              {open &&<CommentsDisabledIcon/>}
            </Style.CommentIconAvatar>

          </Style.CommentMenuWrapper>}
        </Style.CommentListContent>
      </Style.CommentListWrapper>
    {action == "add" && <AddCommentPopup style={{"pointer-events": "initial"}} OnActionClose={onActionClose}/>}
    {action == "update" && <EditCommentPopup style={{"pointer-events": "initial"}} OnActionClose={onActionClose} Comment={selectedComment}/>}
    {action == "delete" && <DeleteCommentPopup style={{"pointer-events": "initial"}} OnActionClose={onActionClose} commentId={selectedComment.id}/>}
    </>
  );
}
