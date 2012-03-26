<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"/static/xhtml1-transitional.dtd">
<html xmlns="/static/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta http-equiv="Content-Language" content="en" />
  <link rel="shortcut icon" href="/images/favicon.ico" />
  <title>Blueshop</title>
  <link type="text/css" rel="stylesheet" media="screen" href="/static/stylesheets/style.css">
% if ('admin' in vars()) and (admin):
  <link type="text/css" rel="stylesheet" media="screen" href="/static/stylesheets/admin.css">
%end
</head>

<body>
<div id="header">
  <div id="logo">
    <a href="/">
      <img src="/images/top-logo.png" alt="logo" title="mycompany" />
    </a>
  </div>

  <div id="header1">
% if ('user' in vars()) and (user):
    User: {{user['ragsoc']}} <br />
    email: {{user['email']}}
% end
    <br />
  </div>

  <div class="clearer">&nbsp;</div>
</div>

% if ('flash' in vars()) and flash:
%   if flash['error']:
<div id="error"> {{flash['error']}} </div>
%   end
%
%   if flash['notice']:
<div id="notice"> {{flash['notice']}} </div>
%   end
% end

%if ('error' in vars()) and (error):
<div id="error"> {{error}} </div>
%end

%if ('notice' in vars()) and (notice):
<div id="notice"> {{notice}} </div>
%end

<div id="layour_main">
  %include
  <div class="clearer"></div>
</div>

%include footer_layout

</body>
</html>
