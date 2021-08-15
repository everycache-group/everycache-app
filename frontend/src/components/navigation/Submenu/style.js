import styled from 'styled-components';
import {Link} from 'react-router-dom';


export const SidebarLink = styled(Link)`
    display: flex;
    color: #e1e9fc;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20px;
    height: 60px;
    text-decoration: none;
    font-size: 18px;
    transition: 300ms ease-in-out;

    &:hover {
        background: #252831;
        border-right: 6px solid #632ce4;
        cursor: pointer;
    }
`;

export const SidebarLabel = styled.span`
    margin-left: 16px;
`;

export const DropDownLink = styled(Link)`
    background: #414757;
    height: 60px;
    padding-left: 3rem;
    display: flex;
    align-items: center;
    text-decoration: none;
    color: #f5f5f5;
    font-size: 18px;
    transition: 300ms ease-in-out;

    &:hover {
        background: #632ce4;
        cursor: pointer;
    }
`;

export const DropDownLinkWrapper = styled.div`
    height: ${({subNav}) => (subNav ?  "120px"  : "0px")};
    overflow: hidden;
    transition: 200ms ease-in-out;
`;