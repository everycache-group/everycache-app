import { Link } from "react-router-dom";
import styled from "styled-components";

export const SidebarWrap = styled.div`
  width: 100%;
`;

export const Nav = styled.div`
  background: #15171c;
  height: 80px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  position: fixed;

  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.32);
  //poprawic to
`;

export const SidebarNav = styled.nav`
  background: #15171c;
  width: 250px;
  height: 100vh;
  display: flex;
  justify-content: center;
  position: fixed;
  top: 0;
  left: ${({ sidebar }) => (sidebar ? "0" : "-100%")};
  transition: 300ms ease-in-out;
  z-index: 10;
`;

export const NavIcon = styled(Link)`
  margin-left: 2rem;
  font-size: 2rem;
  height: 80px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  cursor: pointer;
`;
