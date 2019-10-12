// Do a graphql query to get a bunch of sites
// A Functional component with default props. How is this not built in?
import { Bounds } from "viewport-mercator-project";
import { SitesQuery, useSitesQuery } from "../generated/graphql";
import React, {useEffect, useState} from "react";
import { ApolloError } from "apollo-client";

interface SitesDataProps {
  bounds: Bounds;
  render: (sites: SitesQuery["sites"]) => React.ReactElement;
  whileLoading: () => React.ReactElement; // Only renders when loading === true
  onError: (error: ApolloError) => React.ReactElement;
}

type FCDefault<T> = React.FC<T> & { defaultProps: Partial<T> };

// Hook
function useDebounce(value:any, delay:number) {
  // State and setters for debounced value
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    // Update debounced value after delay
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    // Cancel the timeout if value changes (also on delay change or unmount)
    // This is how we prevent debounced value from updating if value is changed ...
    // .. within the delay period. Timeout gets cleared and restarted.
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]); // Only re-call effect if value or delay changes
  return debouncedValue;
}


const SitesData: FCDefault<SitesDataProps> = props => {
  // Construct the query parameters
  const [[south, west], [north, east]] = useDebounce(props.bounds, 300);
  const rect = `(${west}, ${north}), (${east}, ${south}`;
  const [sitesList, setSitesList] = useState<SitesQuery["sites"]>([]);

  // Fetch new data, and if we have any, add it to the sites list
  // Strip the redundant container stuff, since we only ask for the sites
  const { data, loading, error } = useSitesQuery({
    variables: { rect: rect, limit: 100 }
  });

  if (loading) return props.whileLoading();
  if (error) return props.onError(error);

  console.log(data, loading, error);
  if (data && data.sites.length) {
    console.log(data.sites);
    const nonNullSites = data.sites.filter((element, i) => element);
    setSitesList(nonNullSites);
  }

  return props.render(sitesList);
};

SitesData.defaultProps = {
  whileLoading: () => <></>,
  onError: (error: ApolloError) => {
    console.log(error);
    return <></>;
  }
};

export default SitesData;
