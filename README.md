# Unified system of shops

## REST API
* ## Get Token
#### GET `/api/v1/token/`
#### Body:
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  username: <USERNAME (type:str) (REQUIRED)>,
  password: <PASSWORD (type:str) (REQUIRED)>,
}
```
#### Response:
```yaml 
{
  token: <USER_TOKEN (type:str)>,
}
```
* ## Get shops around
#### GET `/api/v1/shops_around/`
#### Headers
```yaml
{
  lat: <LATITUDE (type:float) (REQUIRED)>,
  lng: <LONGTUDE (type:float) (REQUIRED)>,
  radius: <RADIUS (type:float) (km, default:0.5)>
}
```
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
}
```
#### Response
```yaml
{
  shops: [
    ...
    {
      id: <ID_OF_SHOP (type:int)>,
      lat: <LATITUDE (type:float)>,
      lng: <LONGTUDE (type:float)>,
      chain: <CHAIN_OF_SHOP_ID (type:int)>,
      managers: [
        ...
        <USER_ID (type:int)>,
        ...
      ]
    }
    ...
  ]
}
```
* ## Get shops
#### GET `/api/v1/shops/`
#### Headers
```yaml
{
  chain: <CHAIN_OF_SHOPS_ID (type:int)>,
  id: <SHOP_ID (type:int)>,
}
```
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
}
```
#### Response
```yaml
{
  shops: [
    ...
    {
      id: <SHOP_ID (type:int)>,
      lat: <LATITUDE (type:float)>,
      lng: <LONGTUDE (type:float)>,
      chain: <CHAIN__OF_SHOP_ID (type:int)>,
      managers: [
        ...
        <USER_ID (type:int)>,
        ...
      ]
    }
    ...
  ]
}
```
* ## Create a shop
#### POST `/api/v1/shops/`
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  auth_token: <USER_TOKEN (type:str) (REQUIRED)>,
  chain:  <CHAIN_ID (type:int) (REQUIRED)>,
  lat: <LATITUDE (type:float) (REQUIRED)>,
  lng: <LONGTUDE (type:float) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
  shop: {
    id: <SHOP_ID (type:int)>,
    lat: <LATITUDE (type:float)>,
    lng: <LONGTUDE (type:float)>,
    chain: <CHAIN_OF_SHOP_ID (type:int)>,
    managers: [
      ...
      <USER_ID (type:int)>,
      ...
    ]
  }
}
```
* ## Delete a shop
#### DELETE `/api/v1/shops/`
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  auth_token: <USER_TOKEN (type:str) (REQUIRED)>,
  id: <SHOP_ID (type:int) (REQUIRED)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
}
```
* ## Update a shop
#### PATCH `/api/v1/shops/`
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  auth_token: <USER_TOKEN (type:str) (REQUIRED)>,
  id: <SHOP_ID (type:int) (REQUIRED)>,
  chain: <CHAIN_ID (type:int)>,
  lat: <LATITUDE (type:float)>,
  lng: <LONGTUDE (type:float)>,
}
```
#### Response
```yaml
{
  message: <MESSAGE (type:str)>,
}
```
* ## Get managers
#### GET `/api/v1/managers/`
#### Body
```yaml
{
  app_token: <APPLICATION_TOKEN (type:str) (REQUIRED)>,
  auth_token: <USER_TOKEN (type:str) (REQUIRED)>,
  type: <TYPE (type:str) ('chain' or 'shop') (REQUIRED)>
  id: <SHOP_ID (type:int) (REQUIRED)>,
}
```
#### Response
```yaml
{
  managers: [
    ...
      {
        id: <USER_ID (type:int)>,
        username: <USERNAME (type:str)>,
        first_name: <FIRST_NAME (type:str)>,
        last_name: <LAST_NAME (type:str)>,
        email: <EMAIL (type:str)>,
      }
    ...
  ]
}
```