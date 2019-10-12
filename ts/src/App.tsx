import React from "react";
import "./App.css";
import { Box, Flex, Text } from "rebass";
import { Global } from "@emotion/core";

import Map from "./components/map";
import { ApolloProvider } from "react-apollo";
import ApolloClient from "apollo-boost";
import { ApolloProvider as ApolloHooksProvider } from "react-apollo-hooks";
import SitesData from "./components/sitesData";
import { SitesMarkers } from "./components/siteMarker";

require("dotenv").config();


const client = new ApolloClient({ uri: "http://localhost/api/" });

const App: React.FC = () => {
  return (
    <>
      <Global
        styles={{
          html: {
            height: "100%"
          },
          body: {
            height: "100%",
            display: "flex",
            flexDirection: "column"
          },
          "#root": {
            flex: "1 0 auto"
          }
        }}
      />
      <ApolloProvider client={client}>
        <ApolloHooksProvider client={client}>
          <Flex flexDirection="row" height="100%">
            <Box width={1} flex="1 0 auto">
              <Map
                height="100%"
                render={(bounds) => (
                  <>
                    <Text>Wat</Text>
                    <SitesData
                      bounds={bounds}
                      render={sites => <SitesMarkers sites={sites} />}
                    />
                  </>
                )}
              />
            </Box>
          </Flex>
        </ApolloHooksProvider>
      </ApolloProvider>
    </>
  );
};

export default App;
