

const parseJwt = (token) => {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImRxdWlsaXR6c2NoIiwicm9sZSI6InVzZXIiLCJjcmVhdGVkIjoxNjUyOTkwMTM2LCJleHBpcmVzIjoxNzM5MzkwMTM2fQ.5V9wjTWxkwqT2NllatUV8vPZTRK26TRaQJ4F8LFOmW0"

console.log(parseJwt);