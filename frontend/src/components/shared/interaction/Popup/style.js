import styled from "styled-components";
import { AiOutlineClose } from "react-icons/ai";
import Typography from "@mui/material/Typography";

export const Popup = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.2);

  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
`;

export const PopupInner = styled.div`
  position: relative;
  padding: 64px 32px 32px 32px;

  background-color: #fff;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.32);
  border-radius: 15px;
`;

export const CloseIcon = styled(AiOutlineClose)`
  position: absolute;
  top: 16px;
  right: 16px;
  cursor: pointer;
`;

export const TitleText = styled(Typography)`
  position: absolute;
  top: 16px;
  left: 48px;
  font-size: 18px;
`;
