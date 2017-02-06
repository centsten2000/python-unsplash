

class ResultSet(list):
    """A list like object that holds results from a Twitter API query."""


class Model(object):

    def __init__(self, **kwargs):
        self._repr_values = ["id"]

    def parse(self, data):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError

    @classmethod
    def parse_list(cls, data):
        """Parse a list of JSON objects into a result set of model instances."""
        results = ResultSet()
        for obj in data:
            if obj:
                results.append(cls.parse(obj))
        return results

    def __repr__(self):
        items = filter(lambda x: x[0] in self._repr_values, vars(self).items())
        state = ['%s=%s' % (k, repr(v)) for (k, v) in items]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))


class Photo(Model):

    @classmethod
    def parse(cls, data):
        photo = cls()
        for key, value in data.items():
            if key == "user":
                user = User.parse(value)
                setattr(photo, key, user)
            elif key == "exif":
                exif = Exif.parse(value)
                setattr(photo, key, exif)
            elif key == "urls":
                url = Url.parse(value)
                setattr(photo, key, url)
            elif key == "location":
                location = Location.parse(value)
                setattr(photo, key, location)
            elif key == "links":
                link = Link.parse(value)
                setattr(photo, key, link)
            else:
                setattr(photo, key, value)
        return photo


class Exif(Model):

    def __init__(self, **kwargs):
        super(Exif, self).__init__(**kwargs)
        self._repr_values = ["make", "model"]

    @classmethod
    def parse(cls, data):
        exif = cls()
        for key, value in data.items():
            setattr(exif, key, value)
        return exif


class Url(Model):

    def __init__(self, **kwargs):
        super(Url, self).__init__(**kwargs)
        self._repr_values = ["raw"]

    @classmethod
    def parse(cls, data):
        url = cls()
        for key, value in data.items():
            setattr(url, key, value)
        return url


class Link(Model):

    def __init__(self, **kwargs):
        super(Link, self).__init__(**kwargs)
        self._repr_values = ["html"]

    @classmethod
    def parse(cls, data):
        link = cls()
        for key, value in data.items():
            setattr(link, key, value)
        return link


class Location(Model):

    def __init__(self, **kwargs):
        super(Location, self).__init__(**kwargs)
        self._repr_values = ["title"]

    @classmethod
    def parse(cls, data):
        location = cls()
        for key, value in data.items():
            setattr(location, key, value)
        return location


class User(Model):

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self._repr_values = ["id", "name", "username"]

    @classmethod
    def parse(cls, data):
        user = cls()
        for key, value in data.items():
            if key in ["links", "profile_image"]:
                link = Link.parse(value)
                setattr(user, key, link)
            else:
                setattr(user, key, value)
            setattr(user, key, value)
        return user


class Stat(Model):

    def __init__(self, **kwargs):
        super(Stat, self).__init__(**kwargs)
        self._repr_values = ["total_photos",  "photo_downloads"]

    @classmethod
    def parse(cls, data):
        stat = cls()
        for key, value in data.items():
            setattr(stat, key, value)
        return stat


class Collection(Model):

    def __init__(self, **kwargs):
        super(Collection, self).__init__(**kwargs)
        self._repr_values = ["id",  "title"]

    @classmethod
    def parse(cls, data):
        stat = cls()
        for key, value in data.items():
            if key == "cover_photo":
                photo = Photo.parse(value)
                setattr(stat, key, photo)
            elif key == "user":
                user = User.parse(value)
                setattr(stat, key, user)
            else:
                setattr(stat, key, value)
        return stat
