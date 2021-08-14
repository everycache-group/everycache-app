import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import * as FaIcons from 'react-icons/fa'
import * as AiIcons from 'react-icons/ai'
import * as Style from './style.js'


function Sidebar(props) {
    const [sidebar, setSidebar] = useState(false);

    const showSidebar = () => setSidebar(!sidebar);

    return (
        <>
            <Style.nav>
                <Style.navIcon to='#'>
                    <FaIcons.FaBars onClick={showSidebar} />
                </Style.navIcon>
            </Style.nav>
            <Style.sidebarNav>
                <Style.sidebarWrap>
                    <Style.navIcon to='#' >
                        <AiIcons.AiOutlineClose/>
                    </Style.navIcon>
                </Style.sidebarWrap>
            </Style.sidebarNav>
        </>
    )
}

export default Sidebar;
