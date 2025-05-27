import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useWebsite } from "../../../Context/WebsiteContext";

import {
  createCustomSite,
  changeComponents,
  changeDomain,
  removeAlumni,
  changeName,
  getAllAlumni,
  getAllLabManagers,
  getAllLabMembers,
  createNewSiteManager,
  removeSiteManager,
  addLabMember,
  setSiteContactInfo,
  setSiteAboutUs,
  saveLogo,
  saveHomePicture,
  addAlumni,
  changeTemplate,
  generate,
  deleteGalleryImage,
} from "../../../services/Generator";

import axios from "axios";
import { baseApiUrl } from "../../../services/BaseUrl"; // Ensure the path is correct relative to this file

const useChooseComponents = () => {
  const navigate = useNavigate();
  const { websiteData, setWebsite } = useWebsite();
  const [previewImage, setPreviewImage] = useState(null);

  const [domain, setDomain] = useState(websiteData.domain || "");
  const [websiteName, setWebsiteName] = useState(websiteData.websiteName || "");
  const [components, setComponents] = useState(() => {
    return websiteData.components && websiteData.components.length > 0
      ? websiteData.components
      : ["Home"];
  });
  const [template, setTemplate] = useState(websiteData.template || "");
  const [isChanged, setIsChanged] = useState(false);
  const [buttonText, setButtonText] = useState("Save");
  const [googleLink, setGooogleLink] = useState("");

  const [domainError, setDomainError] = useState(false);
  const [step, setStep] = useState(!domain ? 1 : 3);
  const [showContentSidebar, setShowContentSidebar] = useState(false);
  const [componentsSaved, setComponentsSaved] = useState(
    websiteData.components.length > 1
  );
  const [isComponentsSaved, setIsComponentsSaved] = useState(false);
  const [errorMessage, setErrorMessage] = useState(""); // Store error messages
  const [succsessMessage, setSuccsessMessage] = useState(""); // Store error messages
  const [isTempSaved, setTempSaved] = useState(false);
  const [showTransferPopup, setShowTransferPopup] = useState(false);
  const [newCreatorEmail, setNewCreatorEmail] = useState("");
  const [newRoleAfterResignation, setNewRoleAfterResignation] =
    useState("manager");
  const [isLoading, setIsLoading] = useState(false);
  const [save, setSave] = useState("Save");
  const showError = (message) => {
    setErrorMessage(message);
  };

  const [formData, setFormData] = useState({
    domain: websiteData.domain || "",
    websiteName: websiteData.websiteName || "",
    components: websiteData.components || [],
    files: {},
    publicationsFile: null,
    participantsFile: null,
    logo: null,
    homepagephoto: null,
  });

  const [participants, setParticipants] = useState([
    {
      fullName: "", // Initially empty if not set
      email: sessionStorage.getItem("userEmail") || "",
      degree: "",
      isLabManager: true, // The creator is always a manager
    },
  ]);
  const degreeOptions = [
    "Ph.D.",
    "M.Sc.",
    "B.Sc.",
    "Research Assistant",
    "Faculty Member",
  ];

  const [selectedComponent, setSelectedComponent] = useState("AboutUs"); // Default to About Us
  const [showAddForm, setShowAddForm] = useState(false);
  const [newParticipant, setNewParticipant] = useState({
    fullName: "",
    email: "",
    degree: "",
    isLabManager: false,
  });
  const [mediaSaveStatus, setMediaSaveStatus] = useState({
    logo: false,
    homepagephoto: false,
  });

  const [aboutUsContent, setAboutUsContent] = useState(() => {
    return websiteData.about_us || ""; // Load from sessionStorage initially
  });

  const [contactUsData, setContactUsData] = useState(() => {
    const savedData = websiteData.contact_us;
    return savedData ?? { email: "", phone_num: "", address: "" };
  });
  const [about_usSave, setAboutUsSaved] = useState(false);
  const [contactUs_usSave, setcontactUs] = useState(false);

  useEffect(() => {
    const fetchParticipants = async () => {
      let domain = websiteData.domain;
      try {
        const [managers, members, alumni] = await Promise.all([
          getAllLabManagers(domain),
          getAllLabMembers(domain),
          getAllAlumni(domain),
        ]);

        const allParticipants = [
          ...managers.map((participant) => ({
            ...participant,
            isLabManager: true,
            alumni: false,
            isCreator:
              participant.email === sessionStorage.getItem("userEmail"),
          })),
          ...members.map((participant) => ({
            ...participant,
            isLabManager: false,
            alumni: false,
            isCreator: false,
          })),
          ...alumni.map((participant) => ({
            ...participant,
            isLabManager: false,
            alumni: true,
            isCreator: false,
          })),
        ];
        allParticipants.sort(
          (a, b) => (b.isCreator ? 1 : 0) - (a.isCreator ? 1 : 0)
        );
        setParticipants(allParticipants);
      } catch (err) {
        console.error("Error fetching participants:", err);
      }
    };

    fetchParticipants();
  }, [websiteData.domain]);

  useEffect(() => {
    if (sessionStorage.getItem("isLoggedIn") !== "true") {
      navigate("/");
    }
  }, [navigate]);

  const handleNavClick = (componentName) => {
    setSelectedComponent(componentName);
  };

  const toggleLabManager = async (index) => {
    setSave("Save");
    const updatedParticipants = [...participants];
    const participant = updatedParticipants[index];

    const email = participant.email;
    const isLabManager = participant.isLabManager;

    const selfEmail = sessionStorage.getItem("userEmail");

    try {
      if (email === selfEmail && isLabManager) {
        const otherParticipants = participants.filter(
          (p) => p.email !== selfEmail
        );

        if (otherParticipants.length === 0) {
          showError(
            "You must add another participant before quitting as creator."
          );
          return;
        }
        setShowTransferPopup(true);
        return;
      }
      if (!isLabManager) {
        let data = await createNewSiteManager(
          sessionStorage.getItem("sid"),
          email,
          websiteData.domain
        );
        if (data.response === "true") {
          participant.isLabManager = !isLabManager;
          setParticipants(updatedParticipants);
        }
      } else {
        let data = await removeSiteManager(
          sessionStorage.getItem("sid"),
          email,
          websiteData.domain
        );
        console.log(email);
        if (data.response === "true") {
          participant.isLabManager = !isLabManager;
          setParticipants(updatedParticipants);
        }
      }
    } catch (error) {
      console.error("Error toggling lab manager:", error);
      showError("An error occurred while updating the lab manager.");
    }
  };

  const toggleAlumni = async (index) => {
    setSave("Save");
    const updatedParticipants = [...participants];
    const participant = updatedParticipants[index];

    const email = participant.email;
    const islumi = participant.alumni;

    try {
      if (!islumi) {
        let data = await addAlumni(
          sessionStorage.getItem("sid"),
          email,
          websiteData.domain
        );
        if (data.response === "true") {
          participant.alumni = !islumi;
          setParticipants(updatedParticipants);
        }
      } else {
        let data = await removeAlumni(
          sessionStorage.getItem("sid"),
          email,
          websiteData.domain
        );
        console.log(email);
        if (data.response === "true") {
          participant.alumni = !islumi;
          setParticipants(updatedParticipants);
        }
      }
    } catch (error) {
      console.error("Error toggling lab manager:", error);
      showError("An error occurred while updating the lab manager.");
    }
  };

  const removeParticipant = (index) => {
    setSave("Save");
    setParticipants((prevParticipants) =>
      prevParticipants.filter((_, i) => i !== index)
    );
  };

  const handleInputChangeParticipant = (e) => {
    setSave("Save");
    const { name, value, type, checked } = e.target;
    setNewParticipant((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const addParticipantGen = async () => {
    if (
      newParticipant.fullName &&
      newParticipant.degree &&
      newParticipant.email
    ) {
      try {
        const response = await addLabMember(
          sessionStorage.getItem("sid"), // Manager's User ID, assuming this is stored in sessionStorage
          newParticipant.email, // Email of the new participant
          newParticipant.fullName, // Full name of the new participant
          newParticipant.degree, // Degree of the new participant
          websiteData.domain // Domain of the lab
        );

        if (response.response === "true") {
          setParticipants([
            ...participants,
            { ...newParticipant, isLabManager: false },
          ]);
          setNewParticipant({ fullName: "", degree: "", email: "" });
          setShowAddForm(false);
          setSuccsessMessage(
            "Participant added successfully! It might take a while until you will see changes it website"
          );
        } else {
          showError(`Error: ${response.message}`);
        }
      } catch (error) {
        console.error("Error adding participant:", error);
        showError("An error occurred while adding the lab member.");
      }
    } else {
      showError("Please fill all fields.");
    }
  };

  const addParticipant = () => {
    setSave("Save");
    setParticipants((prevParticipants) => {
      if (prevParticipants.length === 0) {
        // First row: Set the creator info (name is empty at first)
        return [
          {
            fullName: "",
            email: sessionStorage.getItem("userEmail") || "",
            degree: "",
            isLabManager: true, // Creator is always a manager
          },
        ];
      } else {
        // Add a new empty row for additional participants
        return [
          ...prevParticipants,
          { fullName: "", email: "", degree: "", isLabManager: false },
        ];
      }
    });
  };

  const handleParticipantChange = (index, field, value) => {
    setSave("Save");
    setParticipants((prevParticipants) => {
      setButtonText("Save");
      const updatedParticipants = [...prevParticipants]; // Copy array

      if (!updatedParticipants[index]) return prevParticipants; // Avoid errors

      updatedParticipants[index] = {
        ...updatedParticipants[index], // Copy object
        [field]: value, // Update specific field
      };

      return updatedParticipants;
    });
  };
  const handleGoogleScolarChange = (value) => {
    setGooogleLink(value);
  };

  const handleAboutUsChange = (e) => {
    setSave("Save");
    setAboutUsSaved(false);
    setAboutUsContent(e.target.value);
  };

  const saveAboutUs = async () => {
    sessionStorage.setItem("AboutUs", aboutUsContent);
    if (websiteData.generated) {
      const response = await setSiteAboutUs(
        sessionStorage.getItem("sid"),
        websiteData.domain,
        aboutUsContent
      );
      if (response.response === "true") {
        // alert('About Us saved successfully');
      } else {
        showError("Error updating About Us: " + response.message);
      }
    }
    setAboutUsSaved(true);
  };

  const handleContactUsChange = (e) => {
    setSave("Save");
    setcontactUs(false);
    const { name, value } = e.target;
    setContactUsData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const saveContactUs = async () => {
    sessionStorage.setItem("ContactUs", JSON.stringify(contactUsData));
    if (websiteData.generated) {
      const response = await setSiteContactInfo(
        sessionStorage.getItem("sid"),
        websiteData.domain,
        contactUsData.address,
        contactUsData.email,
        contactUsData.phone_num
      );
      if (response.response === "true") {
        // alert('Contact information saved successfully');
      } else {
        showError("Error updating Contact Information: " + response.message);
      }
    }
    setcontactUs(true);
  };

  const handleFileChange = (e, component) => {
    setSave("Save");
    const files = e.target.files;
    if (files && files.length > 0) {
      setFormData((prev) => ({
        ...prev,
        files: {
          ...prev.files,
          [component]: component === "gallery" ? [...files] : files[0],
        },
      }));
      setMediaSaveStatus((prev) => ({ ...prev, [component]: false }));
    }
  };

  const handleDownload = (component) => {
    const link = document.createElement("a");
    link.href = `C:\SE\Lab-Site-Generator\Frontend\lab-gen\src\participants.csv`; // Modify as needed
    link.download = `${component}.xlsx`;
    link.click();
  };

  // const handleSubmit = async (component) => {
  //   const component_new = component.replace(" ", "").toLowerCase();

  //   const formDataToSend = new FormData();
  //   formDataToSend.append("domain", domain);
  //   formDataToSend.append("website_name", websiteName);

  //   if (formData.files[component_new]) {
  //     formDataToSend.append(component_new, formData.files[component_new]);
  //   }

  //   try {
  //     const response = await fetch(`${baseApiUrl}/uploadFile`, {
  //       method: "POST",
  //       body: formDataToSend,
  //     });

  //     const contentType = response.headers.get("content-type") || "";

  //     if (contentType.includes("application/json")) {
  //       const data = await response.json();

  //       if (response.ok) {
  //         // ✅ Success
  //         setMediaSaveStatus((prev) => ({ ...prev, [component_new]: true }));

  //         setWebsite((prev) => ({
  //           ...prev,
  //           files: formData.files,
  //         }));

  //         if (websiteData.generated) {
  //           const saveLogoResponse = await saveLogo(
  //             sessionStorage.getItem("sid"),
  //             websiteData.domain
  //           );
  //           console.log(saveLogoResponse);

  //           const savePhotoResponse = await saveHomePicture(
  //             sessionStorage.getItem("sid"),
  //             websiteData.domain
  //           );
  //           console.log(savePhotoResponse);
  //         }
  //       } else {
  //         // ❌ Error response with JSON body
  //         showError("Error: " + (data.error || "Unknown server error"));
  //       }
  //     } else {
  //       // ❌ Server didn't send JSON, probably HTML error page
  //       const rawText = await response.text();
  //       showError("Server error (non-JSON): " + rawText.slice(0, 100));
  //     }
  //   } catch (error) {
  //     // ❌ Network or parsing error
  //     showError("Unexpected Error: " + error.message);
  //   }
  // };

  const handleSubmit = async (component) => {
    const componentKey = component.replace(" ", "").toLowerCase();
    const files = formData.files[componentKey];

    const formDataToSend = new FormData();
    formDataToSend.append("domain", domain);
    formDataToSend.append("website_name", websiteName);

    // --- Handle gallery upload separately
    console.log(files);
    if (componentKey === "gallery" && Array.isArray(files)) {
      files.forEach((file) => {
        formDataToSend.append(componentKey, file);
      });

      try {
        const response = await fetch(`${baseApiUrl}/uploadGalleryImages`, {
          method: "POST",
          body: formDataToSend,
        });

        const contentType = response.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
          const data = await response.json();
          if (response.ok) {
            setMediaSaveStatus((prev) => ({ ...prev, [componentKey]: true }));
          } else {
            showError(
              "Gallery upload failed: " + (data.error || "Unknown error")
            );
          }
        } else {
          const rawText = await response.text();
          showError(
            "Gallery server error (non-JSON): " + rawText.slice(0, 100)
          );
        }
      } catch (error) {
        showError("Gallery upload exception: " + error.message);
      }
      return; // Exit early
    }

    // --- Handle logo and homepagephoto
    if (files) {
      formDataToSend.append(componentKey, files);
    }

    try {
      const response = await fetch(`${baseApiUrl}/uploadFile`, {
        method: "POST",
        body: formDataToSend,
      });

      const contentType = response.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        const data = await response.json();
        if (response.ok) {
          setMediaSaveStatus((prev) => ({ ...prev, [componentKey]: true }));
          setWebsite((prev) => ({ ...prev, files: formData.files }));

          if (websiteData.generated) {
            if (componentKey === "logo") {
              await saveLogo(sessionStorage.getItem("sid"), websiteData.domain);
            } else if (componentKey === "homepagephoto") {
              await saveHomePicture(
                sessionStorage.getItem("sid"),
                websiteData.domain
              );
            }
          }
        } else {
          showError("Upload failed: " + (data.error || "Unknown error"));
        }
      } else {
        const rawText = await response.text();
        showError("Server error (non-JSON): " + rawText.slice(0, 100));
      }
    } catch (error) {
      showError("Unexpected error: " + error.message);
    }
  };

  const handleGenerate = async () => {
    if (websiteData.generated) {
      setSave("Saved");
      return;
    }

    setIsLoading(true); // Show loading popup
    try {
      console.log(websiteData.domain);
      console.log(domain);
      console.log(participants);
      console.log(googleLink);
      const response = await axios.post(
        `${baseApiUrl}generateWebsite`,
        {
          domain: websiteData.domain,
          about_us: aboutUsContent,
          lab_address: contactUsData.address,
          lab_mail: contactUsData.email,
          lab_phone_num: contactUsData.phone_num,
          participants: participants.map((p) => ({
            fullName: p.fullName,
            email: p.email,
            degree: p.degree,
            isLabManager: p.isLabManager,
            alumni: p.alumni || false,
          })),
          creator_scholar_link: googleLink,
        },
        {
          headers: { "Content-Type": "application/json" },
        }
      );

      const data = response.data;
      console.log("Response Data:", data);

      if (data.response === "true") {
        sessionStorage.removeItem("AboutUs");
        sessionStorage.removeItem("ContactUs");
        navigate("/my-account");
      } else {
        showError("Error: " + (data.error || "Unknown error occurred"));
      }
    } catch (error) {
      showError(error);
      alert("Error: " + (error.response?.data?.message || error.message));
    } finally {
      setIsLoading(false); // Hide popup once done
    }
  };

  /////////////////////////
  useEffect(() => {
    if (sessionStorage.getItem("isLoggedIn") !== "true") {
      navigate("/");
    }
  }, [navigate]);

  const handleContinue = async () => {
    if (!domain || !websiteName) {
      showError("Please enter a domain and website name");
      return;
    }
    let data = await createCustomSite(
      domain,
      websiteName,
      components,
      template
    );
    if (data.response === "true") {
      setWebsite({
        ...websiteData,
        domain,
        websiteName,
        components,
        template,
        created: true,
      });
      setIsChanged(false);
      setStep(3);
    } else {
      setErrorMessage("Error:" + data.message);
    }
  };

  const handleDomainChange = (event) => {
    setDomain(event.target.value);
    setIsChanged(true);
  };

  const handleNameChange = (event) => {
    setWebsiteName(event.target.value);
    setIsChanged(true);
  };

  const handleComponentChange = (component) => {
    setComponents((prev) =>
      prev.includes(component)
        ? prev.filter((c) => c !== component)
        : [...prev, component]
    );
    setIsComponentsSaved(false); // Reset button to "Save"
    setIsChanged(true);
  };

  const handleTemplateClick = (templateName) => {
    setTemplate(templateName === template ? "" : templateName);
    setTempSaved(false);
  };
  const handleSveTemplate = async () => {
    console.log(template);

    let data = await changeTemplate(domain, template);
    console.log(data);
    if (data.response === "true") {
      setIsChanged(true);
      setTempSaved(true);
      console.log(template);
    } else {
      showError("Couldn't change template");
    }
  };

  const isValidDomain = (domain) => domain?.trim() !== "";

  const handleSaveComponents = async () => {
    if (components.length <= 1) {
      showError("Please select components");
      return;
    }
    let data = await changeComponents(domain, components);
    if (data.response === "true") {
      setWebsite({ ...websiteData, components });
      setIsComponentsSaved(true); // Reset button to "Save"
      setIsChanged(false);
      setComponentsSaved(true);
    }
  };

  const handleSaveNameAndDomain = async () => {
    if (!isValidDomain(domain)) {
      setDomainError(true);

      return;
    }
    // const response1 = await changeDomain(websiteData.domain, domain);
    // if (response1.response === "false") {
    //   setErrorMessage("Could not save. Domain name is invalid.");
    //   return;
    // }
    await changeName(domain, websiteName);
    setWebsite({ ...websiteData, domain, websiteName });
    setIsChanged(false);
  };
  const confirmQuitAsCreator = async () => {
    if (!newCreatorEmail) {
      showError("Please select a new creator.");
      return;
    }

    try {
      const response = await axios.post(
        `${baseApiUrl}siteCreatorResignationFromGenerator`,
        {
          user_id: sessionStorage.getItem("sid"),
          domain: domain,
          email: newCreatorEmail,
          new_role: newRoleAfterResignation,
        }
      );

      if (response.data.response === "true") {
        setShowTransferPopup(false);
        navigate("/my-account");
      } else {
        showError(response.data.message || "Failed to transfer ownership.");
      }
    } catch (error) {
      showError("An error occurred: " + error.message);
    }
  };

  const handleDeleteGalleryImage = async (imageName) => {
    // const confirmed = window.confirm(
    //   `Are you sure you want to delete "${imageName}"?`
    // );
    // if (!confirmed) return;

    const userId = sessionStorage.getItem("sid");
    const response = await deleteGalleryImage(
      userId,
      websiteData.domain,
      imageName
    );

    if (response.response === "true") {
      setWebsite({
        gallery: websiteData.gallery.filter(
          (img) => img.filename !== imageName
        ),
      });
    } else {
      setErrorMessage(response.error || "Failed to delete image.");
    }
  };

  return {
    domain,
    websiteName,
    components,
    template,
    isChanged,
    domainError,
    step,
    setStep,
    showContentSidebar,
    setShowContentSidebar,
    handleContinue,
    handleDomainChange,
    handleNameChange,
    handleComponentChange,
    handleTemplateClick,
    handleSaveComponents,
    handleSaveNameAndDomain,
    isValidDomain,
    setDomainError,
    websiteData,
    handleFileChange,
    aboutUsContent,
    setAboutUsContent,
    handleAboutUsChange,
    about_usSave,
    contactUs_usSave,
    saveAboutUs,
    saveContactUs,
    contactUsData,
    handleContactUsChange,
    handleDownload,
    handleSubmit,
    participants,
    setParticipants,
    degreeOptions,
    selectedComponent,
    setSelectedComponent,
    handleNavClick,
    showAddForm,
    setShowAddForm,
    newParticipant,
    setNewParticipant,
    handleInputChangeParticipant,
    addParticipant,
    toggleLabManager,
    toggleAlumni,
    handleParticipantChange,
    componentsSaved,
    setComponentsSaved,
    handleGenerate,
    addParticipantGen,
    removeParticipant,
    isComponentsSaved,
    errorMessage,
    setErrorMessage,
    handleSveTemplate,
    isTempSaved,
    setTempSaved,
    mediaSaveStatus,
    buttonText,
    setButtonText,
    showTransferPopup,
    setShowTransferPopup,
    setNewCreatorEmail,
    newCreatorEmail,
    confirmQuitAsCreator,
    newRoleAfterResignation,
    setNewRoleAfterResignation,
    isLoading,
    succsessMessage,
    setSuccsessMessage,
    handleGoogleScolarChange,
    googleLink,
    setSave,
    save,
    formData,
    setFormData,
    previewImage,
    setPreviewImage,
    handleDeleteGalleryImage,
  };
};

export default useChooseComponents;
