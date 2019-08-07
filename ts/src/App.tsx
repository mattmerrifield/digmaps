import React, {useState} from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';
import { ApolloProvider as ApolloHooksProvider } from 'react-apollo-hooks';
import {FaMapMarker} from "react-icons/fa";

import {useSitesQuery} from "./generated/graphql";
import {Marker} from "react-map-gl";


require('dotenv').config();

interface SiteMarkerProps{
 site: {
    modernName?: string
    coordinates: {
        x: number
        y: number
    }
}}

const SiteMarker = (props: SiteMarkerProps) => {

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

interface SitesMarkerProps {
    x1: number
    y1: number
    x2: number
    y2: number

}

const SitesMarkers = (props: SitesMarkerProps) => {

    const {x1, y1, x2, y2 } = props;
    const rect = `(${x1}, ${y1}), (${x2}, ${y2}`;
    const {data, loading, error} = useSitesQuery({variables: {rect: rect}});

    if (data && data.sites) {
        return <>{data.sites.map(
            (site, i) => {
                if (site && site.coordinates) {
                    console.log(site);
                    return <SiteMarker key={i} site={site}/>
                }
            }
        ).filter(
            (element, i) => element
        )}</>
    }
    else {
        return <></>
    }
};


const client = new ApolloClient({uri: 'http://localhost:8000/api/'});

const App: React.FC = () => {
  return (
      <ApolloProvider client={client}>
          <ApolloHooksProvider client={client}>
              <Flex>
                  <Box width={1}>
                      <Map height={1024}>
                          <Flex>
                              <Text>Welcome to Digmaps!</Text>
                          </Flex>
                      </Map>
                  </Box>
              </Flex>
          </ApolloHooksProvider>
      </ApolloProvider>
  );
};

export default App;
