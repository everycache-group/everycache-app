import styled from "styled-components";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Avatar from '@mui/material/Avatar';
import CommentIcon from '@mui/icons-material/Comment';

export const CommentListWrapper = styled.div`
  position: absolute;
  height: 100%;
  right: 0;
  margin 10px 10px;
  width: 25%;
  z-index: 700;
  pointer-events: none;
`

export const CommentListContent = styled.div`
  position: relative;
  height: 100%;
`

export const CommentList = styled(List)`
  width: 100%;
  overflow-y: auto;
  overflow-x: clip;
  height: 85%;
  pointer-events: initial;
`

export const CommentListItem = styled(ListItem)`
`

export const CommentMenuWrapper = styled.div`
  position: absolute;
  bottom: 30px;
  right: 0;
  margin 10px 0;
  display: grid;
  width:100%;
  grid-template-columns: 50% 50%;
  grid-template-row: 100%;
  justify-items: center;
`

export const ListCommentIcon = styled(CommentIcon)`
`

export const CommentIconAvatar = styled(Avatar)`
  pointer-events: initial;
  transition: 0.1s;
  :hover{
    transform: scale(1.1);
  }

`
