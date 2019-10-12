import React, {useState} from "react";
import {Text} from "rebass";
import {Marker} from "react-map-gl";
import {FaMapMarker} from "react-icons/fa";
import {SiteType} from "../generated/graphql";

type SiteMarkerInfo = Pick<SiteType, 'modernName' | 'coordinates'>

interface SiteMarkerProps {
  site: SiteMarkerInfo
}

// A marker for a single site
export const SiteMarker: React.FC<SiteMarkerProps> = (props) => {

  const [name, setName] = useState(<></>);

  const showName = () => setName(<Text>{props.site.modernName}</Text>);
  const hideName = () => setName(<></>);

  return (
    <Marker latitude={props.site.coordinates.y} longitude={props.site.coordinates.x}>
      <FaMapMarker onMouseEnter={showName} onMouseLeave={hideName}/>
      {name}
    </Marker>
  )

};


// All the markers for an array of sites
interface SitesMarkersProps {
  sites: Array<SiteMarkerInfo>
}

export const SitesMarkers: React.FC<SitesMarkersProps> = (props) => {
  return <>
    {props.sites.map((s, i) => <SiteMarker site={s} key={i}/>)}
    </>
};