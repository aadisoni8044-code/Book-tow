/**
 * Netlify Serverless Function: Download Design
 */
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  const designId = event.queryStringParameters?.id;

  if (!designId) {
    return {
      statusCode: 400,
      body: JSON.stringify({ error: 'Missing design ID parameter' })
    };
  }

  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-cache'
    },
    body: JSON.stringify({
      success: true,
      designId,
      downloadUrl: `/api/download-package?id=${designId}`,
      filename: `${designId}-template.zip`
    })
  };
};
