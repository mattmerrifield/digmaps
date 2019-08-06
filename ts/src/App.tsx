import React, {useState} from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';
import { ApolloProvider as ApolloHooksProvider } from 'react-apollo-hooks';
import {FaMapMarker} from "react-icons/fa";

import {SiteType, useSitesQuery} from "./generated/graphql";
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

const SitesList = () => {
    const {data, loading, error} = useSitesQuery({variables: {limit: 100}});

    if (data && data.sites) {
        return <>{data.sites.map(
            (site, i) => {
                if (site && site.coordinates) {
                    console.log(site)
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
                  <Box width={1/2}>
                  <Map height={1024}>
                      <Flex>
                          <Text>Welcome to Digmaps!</Text>
                      </Flex>
                      <SitesList/>
                  </Map>
                  </Box>
                  <Box width={1/2}>
                      <Text>Sites</Text>
                  </Box>
              </Flex>
          </ApolloHooksProvider>
      </ApolloProvider>
  );
};

export default App;
