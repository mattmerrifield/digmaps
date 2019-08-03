import { gql } from 'apollo-boost'

export default gql`
  query Sites($limit: Int!) {
    sites(limit: $limit) {
      id
      modernName
      ancientName
      coordinates {
        x
        y
      }
    }
  }
`