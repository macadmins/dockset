# Dockset

It's like [outset](https://github.com/chilcote/outset), but for your Dock. This wouldn't be possible without 

## Why?

Sometimes you want to add or remove an item from a user's dock when you're running as root. Maybe you're removing an unused piece of software with Munki or you are adding Chrome to a user's Dock during DEP.

## What?

Dockset will add or remove an item to a user's dock either once or all the time.

## Using it

### Setup

This script assumes you have dockutil in `/usr/local/bin`. If you have it somewhere else, add the following to the LaunchAgent:

```
<string>--dockutil</string>
<string>/opt/bin/dockutil</string>
```

### Building

Build this with Munkipkg.

### Directories

Dockset uses four directories - `add-once`, `remove-once`, `add-always`, `remove-always` - all of these live in `/Library/Application Support/dockset`. You should drop a plist in these directories based on how often you want these managed. **Important:** the current user must be able to remove items from `*-once`, so it is easiest to set these to `777`.

#### The plist - adding items

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>path</key>
    <string>/Applications/Google Chrome.pp</string>
    <key>replacing</key>
    <string>Safari</string>
    <key>position</key>
    <string>beginning</string>
    <key>name</key>
    <string>Google Chrome</string>
</dict>
</plist>
```

#### The plist - removing items

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>name</key>
    <string>Safari</string>
</dict>
</plist>
```
