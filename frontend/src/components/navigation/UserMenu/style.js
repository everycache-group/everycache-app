import styled from "styled-components";
import IconButton from "@mui/material/IconButton";

export const UserActionContainer = styled.div`
  display: flex;
  flex-wrap: nowrap;
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
`;

export const TransformIconButton = styled(IconButton)`
  &:hover {
    transform: scale(1.2);
    transition: all 0.1s ease-in-out;
  }
`;
