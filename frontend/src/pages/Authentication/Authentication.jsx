import React from 'react'
import * as Style from './style'
import Register from '../../components/auth/register/Register'

function AuthenticationPage() {
    return (
        <Style.AuthWrapper>
            <Style.AuthContainer>
                <Register />
            </Style.AuthContainer>
        </Style.AuthWrapper>
    )
}

export default AuthenticationPage
