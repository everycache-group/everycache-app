import * as Style from './style.js'
import { SideBarData } from './../../../data/sidebarData'
import React, { useState, useEffect } from 'react'
import * as FaIcons from 'react-icons/fa'
import * as AiIcons from 'react-icons/ai'
import SubMenu from '../Submenu/Submenu.jsx'
import { IconContext } from 'react-icons/lib'


function Sidebar(props) {
    const [sidebar, setSidebar] = useState(true);
    const [token, setToken] = useState("");
    const showSidebar = () => setSidebar(!sidebar);
    
    useEffect(() => {
        //api.create(api.resources.user, { email: 'a@b.com', password: 'qwerty123', role: 'Admin', username: 'bamer', verified: true });
        

    
    }, []);

    return (
        <>
            <IconContext.Provider value={{ color: '#fff'}}>
                <Style.Nav>
                    <Style.NavIcon to='#'> 
                        <FaIcons.FaBars onClick={showSidebar} />
                        <p style={{color:'white'}}>{token}</p>
                    </Style.NavIcon>
                </Style.Nav>

                <Style.SidebarNav sidebar={sidebar}>
                    <Style.SidebarWrap>
                        <Style.NavIcon to='#' >
                            <AiIcons.AiOutlineClose onClick={showSidebar}/>
                        </Style.NavIcon>
                        {SideBarData.map((item, index) => {      
                            return <SubMenu item={item} key={index} />
                        })}
                    </Style.SidebarWrap>
                </Style.SidebarNav>
            </IconContext.Provider>
        </>
    )
}

export default Sidebar;
