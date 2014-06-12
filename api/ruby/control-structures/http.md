---
layout: api-command
language: Ruby
permalink: api/ruby/http/
command: http
io:
    -   - r
        - value
---

# Command syntax #

{% apibody %}
r.http(url[, options]) &rarr; value
{% endapibody %}

# Description #

Retrieve data from the specified URL over HTTP.  The return type depends on what the response contains, as well as the `result_format` option.

__Example:__ Perform an HTTP `GET` and store the result in a table.

```rb
r.table('posts').insert(
    r.http('http://feedthing.com/feed.json', :redirects => 2)
).run(conn);
```

There is also [a tutorial](/docs/external-api-access/) using `r.http`.

# Options #
* `timeout`: Number of seconds to wait before timing out and aborting the operation. Default: 30.

* `reattempts`: Number of retries to make when connection errors or potentially-temporary HTTP errors occur. Default: 5.

* `redirects`: An integer giving the number of redirects and location headers to follow. Default: 1.

* `verify`: Verify the server's SSL certificate, specified as a boolean. Default: true.

* `result_format`: The format the result should be returned in. The values can be `text` (always return as a string), `json` (parse the result as JSON, raising an error if the parsing fails), `jsonp` (parse the result as [padded JSON](http://www.json-p.org/)), or `auto` . The default is `auto`.

    When `result_format` is `auto`, the response body will be parsed according to the `Content-Type` of the response:
    * `application/json` - parse as `json`
    * `application/json-p`, `text/json-p`, `text/javascript` - parse as `jsonp`
    * Anything else - parse as `text`

## Request Options
* `method`: HTTP method to use for the request. One of `GET`, `POST`, `PUT`, `PATCH`, `DELETE` or `HEAD`. Default: `GET`.

* `auth`: Authentication information in the form of an object with key/value pairs indicating the authentication type (in the `type` key) and any required information. Types currently supported are `basic` and `digest` for HTTP Basic and HTTP Digest authentication respectively. If `type` is omitted, `basic` is assumed. Example:

	```rb
	r.http('http://feedthing.com/feed.json',
           :auth => { :type => 'basic', :user => 'fred', :password => 'mxyzptlk' }
	).run(conn)
	```

* `params`: URL parameters to append to the URL as encoded key/value pairs, specified as an object. For example, `{ :query => 'banana', :limit => 2 }` will be appended as `?query=banana&limit=2`. Default: none.

* `header`: Extra header lines to include. The value may be an array of strings or an object. Default: none.

* `data`: Data to send to the server on a `POST`, `PUT`, `PATCH`, or `DELETE` request.

    For `PUT`, `PATCH` and `DELETE` requests, the value will be serialized to JSON and placed in the request body, and the `Content-Type` will be set to `application/json`.

	For `POST` requests, data may be either an object or a string. Objects will be written to the body as form-encoded key/value pairs (values must be numbers, strings, or `nil`). Strings will be put directly into the body.  If `data` is not a string or an object, an error will be thrown.

    If `data` is not specified, no data will be sent.

## Depagination

`r.http` supports depagination, which will request multiple pages in a row and aggregate the results into a stream.  The use of this feature is controlled by the optional arguments `page` and `page_limit`.  Either none or both of these arguments must be provided.

* `page`: This option specifies a function to provide the next URL and/or `params` to request.  The function takes one parameter, an object of the format:

    ```
    {
        "params": object - the URL parameters used in the last request
        "header": object - the HTTP headers of the last response as key/value pairs
        "body": the body of the last response in whichever format `result_format` gave
    }
    ```

    The `header` field will be a parsed version of the header with fields lowercased, like so:

    ```js
    {
        'content-length': "1024",
        'content-type': "application/json",
        'date': "Thu, 1 Jan 1970 00:00:00 GMT",
        'link': {
            'rel="last"': "http://example.com/?page=34",
            'rel="next"': "http://example.com/?page=2"
        }
    }
    ```

    The `page` function may return a string corresponding to the next URL to request, `nil` indicating that there is no more to get, or an object of the format:

    ```
    {
        "url": string - the next URL to request, or nil for no more pages
        "params": object - new URL parameters to use, will be merged with the previous request's params
    }
    ```

    `page` may also specify a built-in function for performing depagination.  At the moment, the only supported built-in is `'link-next'`, which is equivalent to `lambda {|info| info['header']['link']['rel="next"'].default(nil)}`.  Example:

    ```rb
    r.http("https://api.github.com/search/code?q=addClass+user:mozilla",
           :page => 'link-next', :page_limit => 3).run(conn)
    ```


* `page_limit`: an integer specifying the maximum number of requests to issue using the `page` functionality.  0 means no requests will be made, -1 means there is no limit.

# Examples

__Example:__ Perform multiple requests with different parameters.

```rb
r.expr([1, 2, 3]).map{|i|
    r.http('example.com/api', :params => { :user => i })
}.run(conn)
```

__Example:__ Perform a `PUT` request for each item in a table.

```rb
r.table('data').map{|row|
    r.http('example.com/put', :method => 'PUT', :data => row)
}.run(conn)
```

__Example:__ Perform a `POST` request containing a value.

Using form-encoded data:

```rb
r.http('example.com/post', :method => 'POST', :data => r.expr(value)).run(conn)
```

Using JSON data:

```rb
r.http('example.com/post'
       :method => 'POST',
       :data => r.expr(value).coerce_to('string'),
       :header => { 'Content-Type' => 'application/json' }).run(conn)
```

__Example:__ Perform depagination with a custom `page` function.

```rb
r.http('example.com/pages',
       :page => lambda {|info| info['body']['meta']['next'].default(nil)},
       :page_limit => 5).run(conn)
```
