import { Link } from 'react-router-dom';
import styled, {css } from 'styled-components'

export const sidebarWrap = styled.div`
    width: 100%;
`;

export const nav = styled.div`
    background: #15171c;
    height: 80px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
`;

export const sidebarNav = styled.nav`
    background: #15171c;
    width: 250px;
    height: 100vh;
`;

export const navIcon = styled(Link)`
    margin-left: 2rem;
    font-size: 2rem;
    height: 80px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    cursor:pointer;
`;


