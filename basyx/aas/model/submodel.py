
# Copyright (c) 2020 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
This module contains everything needed to model Submodels and define Events according to the AAS metamodel.
"""

import abc
import datetime
from typing import Optional, Set, Iterable, TYPE_CHECKING, List, Type, TypeVar, Generic, Union

from . import base, datatypes

if TYPE_CHECKING:
    from . import aas


class SubmodelElement(base.Referable, base.Qualifiable, base.HasSemantics, base.HasKind,
                      base.HasDataSpecification, metaclass=abc.ABCMeta):
    """
    A submodel element is an element suitable for the description and differentiation of assets.

    *Note:* The concept of type and instance applies to submodel elements. :class:`Properties <.Property>` are special
    submodel elements. The property types are defined in dictionaries (like the IEC Common Data Dictionary or eCl\\@ss),
    they do not have a value. The property type (`kind=Type`) is also called data element type in some standards.
    The property instances (`kind=Instance`) typically have a value. A property instance is also called
    property-value pair in certain standards.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    @abc.abstractmethod
    def __init__(self,
                 id_short: str,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__()
        self.id_short = id_short
        self.display_name: Optional[base.LangStringSet] = display_name
        self.category = category
        self.description: Optional[base.LangStringSet] = description
        self.parent: Optional[base.UniqueIdShortNamespace] = parent
        self.semantic_id: Optional[base.Reference] = semantic_id
        self.qualifier = base.NamespaceSet(self, [("type", True)], qualifier)
        self._kind: base.ModelingKind = kind
        self.extension = base.NamespaceSet(self, [("name", True)], extension)
        self.supplemental_semantic_id: base.ConstrainedList[base.Reference] = \
            base.ConstrainedList(supplemental_semantic_id)
        self.embedded_data_specifications: List[base.EmbeddedDataSpecification] = list(embedded_data_specifications)


class Submodel(base.Identifiable, base.HasSemantics, base.HasKind, base.Qualifiable,
               base.UniqueIdShortNamespace, base.HasDataSpecification):
    """
    A Submodel defines a specific aspect of the asset represented by the AAS.

    A submodel is used to structure the virtual representation and technical functionality of an Administration Shell
    into distinguishable parts. Each submodel refers to a well-defined domain or subject matter. Submodels can become
    standardized and thus become submodel types. Submodels can have different life-cycles.

    :ivar ~.id: The globally unique id of the element.
                            (inherited from :class:`~aas.model.base.Identifiable`)
    :ivar submodel_element: Unordered list of :class:`SubmodelElements <.SubmodelElement>`
    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar administration: Administrative information of an identifiable element. (inherited from
                          :class:`~aas.model.base.Identifiable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_: base.Identifier,
                 submodel_element: Iterable[SubmodelElement] = (),
                 id_short: str = "NotSet",
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 administration: Optional[base.AdministrativeInformation] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        super().__init__()
        self.id: base.Identifier = id_
        self.submodel_element = base.NamespaceSet(self, [("id_short", True)], submodel_element)
        self.id_short = id_short
        self.display_name: Optional[base.LangStringSet] = display_name
        self.category = category
        self.description: Optional[base.LangStringSet] = description
        self.parent: Optional[base.UniqueIdShortNamespace] = parent
        self.administration: Optional[base.AdministrativeInformation] = administration
        self.semantic_id: Optional[base.Reference] = semantic_id
        self.qualifier = base.NamespaceSet(self, [("type", True)], qualifier)
        self._kind: base.ModelingKind = kind
        self.extension = base.NamespaceSet(self, [("name", True)], extension)
        self.supplemental_semantic_id: base.ConstrainedList[base.Reference] = \
            base.ConstrainedList(supplemental_semantic_id)
        self.embedded_data_specifications: List[base.EmbeddedDataSpecification] = list(embedded_data_specifications)


ALLOWED_DATA_ELEMENT_CATEGORIES: Set[str] = {
    "CONSTANT",
    "PARAMETER",
    "VARIABLE"
}


class DataElement(SubmodelElement, metaclass=abc.ABCMeta):
    """
    A data element is a :class:`~.SubmodelElement` that is not further composed out of other
    :class:`SubmodelElements <.SubmodelElement>`.
    A data element is a :class:`~.SubmodelElement` that has a value. The type of value differs for different subtypes
    of data elements.

    <<abstract>>

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    @abc.abstractmethod
    def __init__(self,
                 id_short: str,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)

    def _set_category(self, category: Optional[str]):
        if category == "":
            raise base.AASConstraintViolation(100,
                                              "category is not allowed to be an empty string")
        if category is None:
            self._category = None
        else:
            if category not in ALLOWED_DATA_ELEMENT_CATEGORIES:
                if not (isinstance(self, File) or isinstance(self, Blob)):
                    raise base.AASConstraintViolation(
                        90,
                        "DataElement.category must be one of the following: " +
                        ", ".join(ALLOWED_DATA_ELEMENT_CATEGORIES))
            self._category = category


class Property(DataElement):
    """
    A property is a :class:`DataElement` that has a single value.

    *Constraint AASd-007:* if both, the value and the valueId are present then the value needs to be
    identical to the value of the referenced coded value in valueId

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar value_type: Data type of the value
    :ivar value: The value of the property instance.
    :ivar value_id: :class:`~aas.model.base.Reference` to the global unique id of a coded value
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 value_type: base.DataTypeDefXsd,
                 value: Optional[base.ValueDataType] = None,
                 value_id: Optional[base.Reference] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value_type: base.DataTypeDefXsd = value_type
        self._value: Optional[base.ValueDataType] = (datatypes.trivial_cast(value, value_type)
                                                     if value is not None else None)
        self.value_id: Optional[base.Reference] = value_id

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value) -> None:
        if value is None:
            self._value = None
        else:
            self._value = datatypes.trivial_cast(value, self.value_type)


class MultiLanguageProperty(DataElement):
    """
    A multi language property is a :class:`~.DataElement` that has a multi language value.

    *Constraint AASd-012*: if both, the value and the valueId are present then for each string in a
    specific language the meaning must be the same as specified in valueId.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar value: The value of the property instance.
    :ivar value_id: :class:`~aas.model.base.Reference` to the global unique id of a coded value
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 value: Optional[base.LangStringSet] = None,
                 value_id: Optional[base.Reference] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value: Optional[base.LangStringSet] = value
        self.value_id: Optional[base.Reference] = value_id


class Range(DataElement):
    """
    A range is a :class:`~.DataElement` that has a range value.

    *Constraint AASd-013:* In case of a range with `kind=Instance` either the min or the max value or both
    need to be defined

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar value_type: Data type of the min and max
    :ivar min: The minimum value of the range. If the min value is missing then the value is assumed to be negative
               infinite
    :ivar max: The maximum of the range. If the max value is missing then the value is assumed to be positive infinite
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 value_type: base.DataTypeDefXsd,
                 min: Optional[base.ValueDataType] = None,
                 max: Optional[base.ValueDataType] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value_type: base.DataTypeDefXsd = value_type
        self._min: Optional[base.ValueDataType] = datatypes.trivial_cast(min, value_type) if min is not None else None
        self._max: Optional[base.ValueDataType] = datatypes.trivial_cast(max, value_type) if max is not None else None

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value) -> None:
        if value is None:
            self._min = None
        else:
            self._min = datatypes.trivial_cast(value, self.value_type)

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value) -> None:
        if value is None:
            self._max = None
        else:
            self._max = datatypes.trivial_cast(value, self.value_type)


class Blob(DataElement):
    """
    A BLOB is a :class:`~.DataElement` that represents a file that is contained with its source code in the value
    attribute.

    *Note:* In contrast to the file property the file content is stored directly as value in the Blob data element.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar content_type: Mime type of the content of the BLOB. The mime type states which file extension the file has.
                     Valid values are e.g. “application/json”, “application/xls”, ”image/jpg”. The allowed values
                     are defined as in RFC2046.
    :ivar value: The value of the BLOB instance of a blob data element.
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 content_type: base.ContentType,
                 value: Optional[base.BlobType] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value: Optional[base.BlobType] = value
        self.content_type: base.ContentType = content_type


class File(DataElement):
    """
    A File is a :class:`~.DataElement` that represents a file via its path description.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar content_type: Mime type of the content of the File.
    :ivar value: Path and name of the referenced file (with file extension). The path can be absolute or relative.
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 content_type: base.ContentType,
                 value: Optional[base.PathType] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value: Optional[base.PathType] = value
        self.content_type: base.ContentType = content_type


class ReferenceElement(DataElement):
    """
    A reference element is a :class:`DataElement` that defines a :class:`~aas.model.base.Reference` to another element
    within the same or another AAS or a :class:`~aas.model.base.Reference` to an external object or entity.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar value: :class:`~aas.model.base.Reference` to any other :class:`~aas.model.base.Referable` element of the same
                 or any other AAS or a :class:`~aas.model.base.Reference` to an external object or entity.
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 value: Optional[base.Reference] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value: Optional[base.Reference] = value


class SubmodelElementCollection(SubmodelElement, base.UniqueIdShortNamespace):
    """
    A submodel element collection is a set or list of :class:`SubmodelElements <.SubmodelElement>`.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar value: list of :class:`SubmodelElements <.SubmodelElement>`
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 value: Iterable[SubmodelElement] = (),
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.value: base.NamespaceSet[SubmodelElement] = base.NamespaceSet(self, [("id_short", True)], value)


_SE = TypeVar("_SE", bound=SubmodelElement)


class SubmodelElementList(SubmodelElement, base.UniqueIdShortNamespace, Generic[_SE]):
    """
    A submodel element list is an ordered list of :class:`SubmodelElements <.SubmodelElement>`.
    The numbering starts with Zero (0).

    *Constraint AASd-107:* If a first level child element in a :class:`SubmodelElementList` has a semanticId it shall be
    identical to SubmodelElementList/semanticIdListElement.
    *Constraint AASd-114:* If two first level child elements in a :class:`SubmodelElementList` have a semanticId then
    they shall be identical.
    *Constraint AASd-115:* If a first level child element in a :class:`SubmodelElementList` does not specify
    a semanticId then the value is assumed to be identical to SubmodelElementList/semanticIdListElement.
    *Constraint AASd-108:* All first level child elements in a :class:`SubmodelElementList` shall have the same
    submodel element type as specified in SubmodelElementList/typeValueListElement.
    *Constraint AASd-109:* If SubmodelElementList/typeValueListElement equal to Property or Range
    SubmodelElementList/valueTypeListElement shall be set and all first level child elements in the
    :class:`SubmodelElementList` shall have the value type as specified in SubmodelElementList/valueTypeListElement.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar type_value_list_element: The :class:`SubmodelElement` type of the submodel elements contained in the list.
    :ivar value: :class:`SubmodelElements <.SubmodelElement>` contained in the list. The list is ordered.
    :ivar semantic_id_list_element: Semantic ID of the :class:`SubmodelElements <.SubmodelElement>` contained in the
                                    list to match to.
    :ivar value_type_list_element: The value type of the submodel element contained in the list.
    :ivar order_relevant: Defines whether order in list is relevant. If False the list is representing a set or a bag.
                          Default: True
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 type_value_list_element: Type[_SE],
                 value: Iterable[_SE] = (),
                 semantic_id_list_element: Optional[base.Reference] = None,
                 value_type_list_element: Optional[base.DataTypeDefXsd] = None,
                 order_relevant: bool = True,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        # It doesn't really make sense to change any of these properties. thus they are immutable here.
        self._type_value_list_element: Type[_SE] = type_value_list_element
        self._order_relevant: bool = order_relevant
        self._semantic_id_list_element: Optional[base.Reference] = semantic_id_list_element
        self._value_type_list_element: Optional[base.DataTypeDefXsd] = value_type_list_element

        if self.type_value_list_element in (Property, Range) and self.value_type_list_element is None:
            raise base.AASConstraintViolation(109, f"type_value_list_element={self.type_value_list_element.__name__}, "
                                                   "but value_type_list_element is not set!")

        # Items must be added after the above contraint has been checked. Otherwise, it can lead to errors, since the
        # constraints in _check_constraints() assume that this constraint has been checked.
        self._value: base.OrderedNamespaceSet[_SE] = base.OrderedNamespaceSet(self, [("id_short", True)], value,
                                                                              self._check_constraints)

    def _check_constraints(self, new: _SE, existing: Iterable[_SE]) -> None:
        # We can't use isinstance(new, self.type_value_list_element) here, because each subclass of
        # self.type_value_list_element wouldn't raise a ConstraintViolation, when it should.
        # Example: AnnotatedRelationshipElement is a subclass of RelationshipElement
        if type(new) is not self.type_value_list_element:
            raise base.AASConstraintViolation(108, "All first level elements must be of the type specified in "
                                                   f"type_value_list_element={self.type_value_list_element.__name__}, "
                                                   f"got {new!r}")

        if self.semantic_id_list_element is not None and new.semantic_id is not None \
                and new.semantic_id != self.semantic_id_list_element:
            # Constraint AASd-115 specifies that if the semantic_id of an item is not specified
            # but semantic_id_list_element is, the semantic_id of the new is assumed to be identical.
            # Not really a constraint...
            # TODO: maybe set the semantic_id of new to semantic_id_list_element if it is None
            raise base.AASConstraintViolation(107, f"If semantic_id_list_element={self.semantic_id_list_element!r} "
                                                   "is specified all first level children must have the same "
                                                   f"semantic_id, got {new!r} with semantic_id={new.semantic_id!r}")

        # If we got here we know that `new` is an instance of type_value_list_element and that type_value_list_element
        # is either Property or Range. Thus, `new` must have the value_type property. Ignore the type here because
        # the typechecker doesn't get it.
        if self.type_value_list_element in (Property, Range) \
                and new.value_type is not self.value_type_list_element:  # type: ignore
            raise base.AASConstraintViolation(109, "All first level elements must have the value_type "  # type: ignore
                                                   "specified by value_type_list_element="
                                                   f"{self.value_type_list_element.__name__}, got {new!r} with "
                                                   f"value_type={new.value_type.__name__}")  # type: ignore

        # If semantic_id_list_element is not None that would already enforce the semantic_id for all first level
        # elements. Thus, we only need to perform this check if semantic_id_list_element is None.
        if new.semantic_id is not None and self.semantic_id_list_element is None:
            for item in existing:
                if item.semantic_id is not None and new.semantic_id != item.semantic_id:
                    raise base.AASConstraintViolation(114, f"Element to be added {new!r} has semantic_id "
                                                           f"{new.semantic_id!r}, while already contained element "
                                                           f"{item!r} has semantic_id {item.semantic_id!r}, which "
                                                           "aren't equal.")

    @property
    def value(self) -> base.OrderedNamespaceSet[_SE]:
        return self._value

    @value.setter
    def value(self, value: Iterable[_SE]):
        del self._value[:]
        self._value.extend(value)

    @property
    def type_value_list_element(self) -> Type[_SE]:
        return self._type_value_list_element

    @property
    def order_relevant(self) -> bool:
        return self._order_relevant

    @property
    def semantic_id_list_element(self) -> Optional[base.Reference]:
        return self._semantic_id_list_element

    @property
    def value_type_list_element(self) -> Optional[base.DataTypeDefXsd]:
        return self._value_type_list_element


class RelationshipElement(SubmodelElement):
    """
    A relationship element is used to define a relationship between two :class:`~aas.model.base.Referable` elements.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar first: Reference to the first element in the relationship taking the role of the subject which have to
                 be of class Referable. (inherited from :class:`~.RelationshipElement`)
    :ivar second: Reference to the second element in the relationship taking the role of the object which have to
                  be of class Referable. (inherited from :class:`~.RelationshipElement`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 first: base.Reference,
                 second: base.Reference,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.first: base.Reference = first
        self.second: base.Reference = second


class AnnotatedRelationshipElement(RelationshipElement, base.UniqueIdShortNamespace):
    """
    An annotated relationship element is a :class:`~.RelationshipElement` that can be annotated
    with additional :class:`DataElements <.DataElement>`.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar first: Reference to the first element in the relationship taking the role of the subject which have to
                 be of class Referable. (inherited from :class:`~.RelationshipElement`)
    :ivar second: Reference to the second element in the relationship taking the role of the object which have to
                  be of class Referable. (inherited from :class:`~.RelationshipElement`)
    :ivar annotation: Unordered list of :class:`DataElements <.DataElement>` that hold for the relationship between two
                      elements
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 first: base.Reference,
                 second: base.Reference,
                 display_name: Optional[base.LangStringSet] = None,
                 annotation: Iterable[DataElement] = (),
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, first, second, display_name, category, description, parent, semantic_id, qualifier,
                         kind, extension, supplemental_semantic_id, embedded_data_specifications)
        self.annotation = base.NamespaceSet(self, [("id_short", True)], annotation)


class OperationVariable:
    """
    An operation variable is part of an operation that is used to define an input or output variable of that operation.

    :ivar value: Describes the needed argument for an operation via a :class:`~.SubmodelElement` of `kind=TYPE`.
    """

    def __init__(self,
                 value: SubmodelElement):
        """
        TODO: Add instruction what to do after construction
        """
        self.value: SubmodelElement = value


class Operation(SubmodelElement):
    """
    An operation is a :class:`~.SubmodelElement` with input and output variables.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar input_variable: List of input parameters (:class:`OperationVariables <.OperationVariable>`) of the operation
    :ivar output_variable: List of output parameters (:class:`OperationVariables <.OperationVariable>`) of the operation
    :ivar in_output_variable: List of parameters (:class:`OperationVariables <.OperationVariable>`) that are input and
                              output of the operation
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 input_variable: Optional[List[OperationVariable]] = None,
                 output_variable: Optional[List[OperationVariable]] = None,
                 in_output_variable: Optional[List[OperationVariable]] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.input_variable = input_variable if input_variable is not None else []
        self.output_variable = output_variable if output_variable is not None else []
        self.in_output_variable = in_output_variable if in_output_variable is not None else []


class Capability(SubmodelElement):
    """
    A capability is the implementation-independent description of the potential of an asset to achieve a certain effect
    in the physical or virtual world

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                    It affects the expected existence of attributes and the applicability of constraints.
                    (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)


class Entity(SubmodelElement, base.UniqueIdShortNamespace):
    """
    An entity is a :class:`~.SubmodelElement` that is used to model entities

    *Constraint AASd-014:* global_asset_id or specific_asset_id must be set if :attr:`~.entity_type` is set to
    :attr:`~.EntityType.SELF_MANAGED_ENTITY`. They must be empty otherwise.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar entity_type: Describes whether the entity is a co-managed or a self-managed entity.
    :ivar statement: Unordered list of statements (:class:`SubmodelElements <.SubmodelElement>`) applicable to the
                     entity, typically with a qualified value.
    :ivar global_asset_id: :class:`~aas.model.base.Reference` to the asset the AAS is
                           representing. This attribute is required as soon as the AAS is exchanged via partners
                           in the life cycle of the asset. In a first phase of the life cycle the asset might not
                           yet have a global id but already an internal identifier. The internal identifier would
                           be modelled via “specificAssetId”.
    :ivar specific_asset_id: :class:`~aas.model.base.Reference` to an identifier key value pair representing a specific
                             identifier
                             of the asset represented by the asset administration shell. See Constraint AASd-014
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 entity_type: base.EntityType,
                 statement: Iterable[SubmodelElement] = (),
                 global_asset_id: Optional[base.GlobalReference] = None,
                 specific_asset_id: Optional[base.SpecificAssetId] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """
        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.statement = base.NamespaceSet(self, [("id_short", True)], statement)
        self.specific_asset_id: Optional[base.SpecificAssetId] = specific_asset_id
        self.global_asset_id: Optional[base.GlobalReference] = global_asset_id
        self._entity_type: base.EntityType
        self.entity_type = entity_type

    def _get_entity_type(self) -> base.EntityType:
        return self._entity_type

    def _set_entity_type(self, entity_type: base.EntityType) -> None:
        if self.global_asset_id is None and self.specific_asset_id is None \
                and entity_type == base.EntityType.SELF_MANAGED_ENTITY:
            raise base.AASConstraintViolation(
                14,
                "A self-managed entity has to have a globalAssetId or a specificAssetId"
            )
        if (self.global_asset_id or self.specific_asset_id) and entity_type == base.EntityType.CO_MANAGED_ENTITY:
            raise base.AASConstraintViolation(
                14,
                "A co-managed entity has to have neither a globalAssetId nor a specificAssetId")
        self._entity_type = entity_type

    entity_type = property(_get_entity_type, _set_entity_type)


class EventElement(SubmodelElement, metaclass=abc.ABCMeta):
    """
    An event element.
    <<abstract>>

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from
                     :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    @abc.abstractmethod
    def __init__(self,
                 id_short: str,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)


class BasicEventElement(EventElement):
    """
    A basic event element.

    :ivar id_short: Identifying string of the element within its name space. (inherited from
                    :class:`~aas.model.base.Referable`)
    :ivar observed: :class:`~aas.model.base.ModelReference` to the Referable, which defines the scope of the event.
                    Can be :class:`~aas.model.aas.AssetAdministrationShell`, :class:`~aas.model.submodel.Submodel`
                    or :class:`~aas.model.submodel.SubmodelElement`. Reference to a referable, e.g. a data element
                    or a submodel, that is being observed.
    :ivar direction: Direction of event as :class:`~aas.model.base.Direction`.
    :ivar state: State of event as :class:`~aas.model.base.StateOfEvent`.
    :ivar message_topic: Information for the outer message infrastructure for scheduling the event to the respective
                         communication channel.
    :ivar message_broker: Information, which outer message infrastructure shall handle messages for the EventElement.
                          Refers to a :class:`~aas.model.submodel.Submodel`,
                          :class:`~aas.model.submodel.SubmodelElementList`,
                          :class:`~aas.model.submodel.SubmodelElementCollection` or :class:`~aas.model.submodel.Entity`,
                          which contains DataElements describing the proprietary specification for the message broker.
                          Note: for different message infrastructure, e.g. OPC UA or MQTT or AMQP, this proprietary
                          specification could be standardized by having respective Submodels.
    :ivar last_update: Timestamp in UTC, when the last event was received (input direction) or sent (output direction).
    :ivar min_interval: For input direction, reports on the maximum frequency, the software entity behind the respective
                        Referable can handle input events. For output events, specifies the maximum frequency of
                        outputting this event to an outer infrastructure.
    :ivar max_interval: For input direction: not applicable.
                        For output direction: maximum interval in time, the respective Referable shall send an update of
                        the status of the event, even if no other trigger condition for the event was not met.
    :ivar display_name: Can be provided in several languages. (inherited from :class:`~aas.model.base.Referable`)
    :ivar category: The category is a value that gives further meta information w.r.t. to the class of the element.
                     It affects the expected existence of attributes and the applicability of constraints.
                     (inherited from :class:`~aas.model.base.Referable`)
    :ivar description: Description or comments on the element. (inherited from :class:`~aas.model.base.Referable`)
    :ivar parent: Reference to the next referable parent element of the element. (inherited from
                  :class:`~aas.model.base.Referable`)
    :ivar semantic_id: Identifier of the semantic definition of the element. It is called semantic id of the
                       element. The semantic id may either reference an external global id or it may reference a
                       referable model element of kind=Type that defines the semantics of the element.
                       (inherited from :class:`~aas.model.base.HasSemantics`)
    :ivar qualifier: Unordered list of Qualifiers that gives additional qualification of a qualifiable element.
                     (from :class:`~aas.model.base.Qualifiable`)
    :ivar kind: Kind of the element: Either `TYPE` or `INSTANCE`. Default is `INSTANCE`. (inherited from
                :class:`aas.model.base.HasKind`)
    :ivar extension: An extension of the element. (inherited from :class:`aas.model.base.HasExtension`)
    :ivar supplemental_semantic_id: Identifier of a supplemental semantic definition of the element. It is called
                                    supplemental semantic ID of the element. (inherited from
                                    :class:`~aas.model.base.HasSemantics`)
    :ivar embedded_data_specifications: List of Embedded data specification.
    """

    def __init__(self,
                 id_short: str,
                 observed: base.ModelReference[Union["aas.AssetAdministrationShell", Submodel, SubmodelElement]],
                 direction: base.Direction,
                 state: base.StateOfEvent,
                 message_topic: Optional[str] = None,
                 message_broker: Optional[base.ModelReference[Union[Submodel, SubmodelElementList,
                                                                    SubmodelElementCollection, Entity]]] = None,
                 last_update: Optional[datatypes.DateTime] = None,
                 min_interval: Optional[datatypes.Duration] = None,
                 max_interval: Optional[datatypes.Duration] = None,
                 display_name: Optional[base.LangStringSet] = None,
                 category: Optional[str] = None,
                 description: Optional[base.LangStringSet] = None,
                 parent: Optional[base.UniqueIdShortNamespace] = None,
                 semantic_id: Optional[base.Reference] = None,
                 qualifier: Iterable[base.Qualifier] = (),
                 kind: base.ModelingKind = base.ModelingKind.INSTANCE,
                 extension: Iterable[base.Extension] = (),
                 supplemental_semantic_id: Iterable[base.Reference] = (),
                 embedded_data_specifications: Iterable[base.EmbeddedDataSpecification] = ()):
        """
        TODO: Add instruction what to do after construction
        """

        super().__init__(id_short, display_name, category, description, parent, semantic_id, qualifier, kind, extension,
                         supplemental_semantic_id, embedded_data_specifications)
        self.observed: base.ModelReference[Union["aas.AssetAdministrationShell", Submodel, SubmodelElement]] = observed
        # max_interval must be set here because the direction setter attempts to read it
        self.max_interval: Optional[datatypes.Duration] = None
        self.direction: base.Direction = direction
        self.state: base.StateOfEvent = state
        self.message_topic: Optional[str] = message_topic
        self.message_broker: Optional[base.ModelReference[Union[Submodel, SubmodelElementList,
                                                                SubmodelElementCollection, Entity]]] = message_broker
        self.last_update: Optional[datatypes.DateTime] = last_update
        self.min_interval: Optional[datatypes.Duration] = min_interval
        self.max_interval: Optional[datatypes.Duration] = max_interval

    @property
    def direction(self) -> base.Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: base.Direction) -> None:
        if direction is base.Direction.INPUT and self.max_interval is not None:
            raise ValueError("max_interval is not applicable if direction = input!")
        self._direction: base.Direction = direction

    @property
    def last_update(self) -> Optional[datatypes.DateTime]:
        return self._last_update

    @last_update.setter
    def last_update(self, last_update: Optional[datatypes.DateTime]) -> None:
        if last_update is not None and last_update.tzname() != "UTC":
            raise ValueError("last_update must be specified in UTC!")
        self._last_update: Optional[datatypes.DateTime] = last_update

    @property
    def max_interval(self) -> Optional[datatypes.Duration]:
        return self._max_interval

    @max_interval.setter
    def max_interval(self, max_interval: Optional[datatypes.Duration]) -> None:
        if max_interval is not None and self.direction is base.Direction.INPUT:
            raise ValueError("max_interval is not applicable if direction = input!")
        self._max_interval: Optional[datatypes.Duration] = max_interval


class EventPayload:
    """
    Defines the necessary information of an event instance sent out or received.

    :ivar source :class:`~aas.model.base.ModelReference` Reference to the source event element. It is of type
                  class:`~aas.model.submodel.EventElement`.
    :ivar observable_reference: class:`~aas.model.base.ModelReference` semanticId of the source event element,
                               if available.
    :ivar timestamp: class:`datatypes.DateTime` Timestamp in UTC, when this event was triggered.
    :ivar source_semantic_id: class:`~aas.model.base.ModelReference` semanticId of the source event element, if
    available.
    :ivar topic: class: `datatypes.MessageTopicType`: Information for the outer message infrastructure to schedule
    the event for the respective communication channel.
    :ivar subject_id :class:`~aas.model.base.ModelReference`: Subject, who/which initiated the creation.
    :ivar payload: Event-specific payload.
    """
    def __init__(self, source: base.ModelReference[EventElement],
                 observable_reference: base.ModelReference[base.Referable],
                 timestamp: datatypes.DateTime,
                 source_semantic_id: Optional[base.Reference] = None,
                 observable_semantic_id: Optional[base.Reference] = None,
                 topic: Optional[base.MessageTopicType] = None,
                 subject_id: Optional[base.Reference] = None,
                 payload: Optional[base.BlobType] = None):
        self.source: base.ModelReference[EventElement] = source
        self.observable_reference: base.ModelReference[base.Referable] = observable_reference
        self.timestamp: datatypes.DateTime = timestamp
        self.source_semantic_id: Optional[base.Reference] = source_semantic_id
        self.observable_semantic_id: Optional[base.Reference] = observable_semantic_id
        self.topic: Optional[base.MessageTopicType] = topic
        self.subject_id: Optional[base.Reference] = subject_id
        self.payload: Optional[base.BlobType] = payload

    @property
    def timestamp(self) -> Optional[datatypes.DateTime]:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datatypes.DateTime) -> None:
        if timestamp is not None and timestamp.tzname() != "UTC":
            raise ValueError("timestamp must be specified in UTC!")
        self._timestamp: Optional[datatypes.DateTime] = timestamp
