import "./App.css"
import  img from "./images/missile.png"

function Header() { 
   
    return (<div className="header">
        <div className="header">
            <div className="logo">
                <img src={img} alt="logo" />
                <div className="logo-content">
                    <p style={{fontSize:10}}>M . I . D . A . S</p>
                    <p id="description">Missile Interception Decision Analysis System</p>

                </div>
            </div>
            
        </div>
    
</div>)

}
export default Header