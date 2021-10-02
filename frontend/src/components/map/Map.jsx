import mapCSS from "./Map.module.css";
import React from "react";
import { MapContainer, TileLayer, Marker, Tooltip } from "react-leaflet";
import { useState} from 'react'

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      areCachesLoaded: false,
      areUsersLoaded: false,
      caches: [],
      users: [],
    };
  }

  const [cachesLoaded, setCachesLoaded] = useState(false);


  setCachesLoaded(true);

  componentDidMount() {
    var backend_url =
      process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";
    fetch(`${backend_url}/caches`)
      .then((res) => res.json())
      .then((result) => {
        this.setState({
          caches: result.caches,
          areCachesLoaded: true,
        });
      });
    fetch(`${backend_url}/users`)
      .then((res) => res.json())
      .then((result) => {
        this.setState({
          users: result.users,
          areUsersLoaded: true,
        });
      });
  }

  render() {
    const { areCachesLoaded, areUsersLoaded, caches, users } = this.state;
    if (!areCachesLoaded || !areUsersLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <MapContainer
          id="mapid"
          center={[caches[0].lat, caches[0].lon]}
          zoom={13}
        >
          <TileLayer
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {caches.map((cache) => (
            <Marker position={{ lat: cache.lat, lon: cache.lon }}>
              <Tooltip>
                <span style={{ fontSize: 16 }}>
                  <b>{cache.name}</b>
                </span>
                <br />
                {cache.created_at}
                <br />
                <br />
                <b>Owner: </b>
                {users[cache.owner_id - 1].name}
                <br />
                <b>Description: </b>
                <br />
                {cache.description.split("\n").map((i, key) => {
                  return <div key={key}>{i}</div>;
                })}
              </Tooltip>
            </Marker>
          ))}
        </MapContainer>
      );
    }
  }
}

export default Map;
