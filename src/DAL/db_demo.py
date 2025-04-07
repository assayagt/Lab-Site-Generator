import logging
import uuid

import sys
import os

# Print current directory for debugging
print(f"Current directory: {os.getcwd()}")
print(f"File directory: {os.path.dirname(os.path.abspath(__file__))}")

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
print(f"Added to path: {project_root}")
print(f"System path now: {sys.path}")
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO


from DAL_controller import DAL_controller

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Remove existing database file for a clean demo
    db_path = 'LSG.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"Removed existing database file: {db_path}")

    dal_controller = DAL_controller()
    pub_repo = dal_controller.publications_repo
    
    # Initialize database manager
    #db_manager = DatabaseManager(db_path)

    logger.info("Database tables created")

    # Create a sample publication
    pub_id = str(uuid.uuid4())
    sample_pub = PublicationDTO(
        paper_id=pub_id,
        title="Lab Site Generator: A Modern Approach to Research Website Creation",
        authors="Jane Doe, John Smith",
        publication_year=2024,
        approved="Yes",
        publication_link="https://example.com/paper",
        git_link="https://github.com/example/lsg",
        video_link="https://youtu.be/example",
        presentation_link="https://example.com/presentation",
        description="This paper presents a novel approach to generating research lab websites."
    )

    # Save the publication
    success = pub_repo.save(sample_pub, 'example domain')
    logger.info(f"Publication saved: {success}")

    # Create another sample publication
    sample_pub2 = PublicationDTO(
       paper_id=str(uuid.uuid4()),
        title="User Experience in Academic Websites",
        authors="Alice Johnson, Bob Brown",
        publication_year=2023,
        approved="Yes",
        publication_link="https://example.com/paper2",
        description="A study on user experience in academic and research websites."
    )
    # Save the second publication
    success = pub_repo.save(sample_pub2, 'example domain')
    logger.info(f"Second publication saved: {success}")

    # Find by ID
    found_pub = pub_repo.find_by_id(pub_id)
    if found_pub:
        logger.info(f"Found publication by ID: {found_pub}")
    else:
        logger.error("Publication not found")

    # Get all publications
    all_pubs = pub_repo.find_all()
    logger.info(f"Found {len(all_pubs)} publications")

    # Print all publications
    for i, pub in enumerate(all_pubs, 1):
        logger.info(f"Publication {i}: {pub}")

    # Update a publication
    if found_pub:
        found_pub.title = "UPDATED: " + found_pub.title
        success = pub_repo.save(found_pub)
        logger.info(f"Publication updated: {success}")
    
    # Verify update
    updated_pub = pub_repo.find_by_id(pub_id)
    if updated_pub:
        logger.info(f"Updated publication: {updated_pub}")
    
    # Delete a publication
    if updated_pub:
        success = pub_repo.delete(updated_pub.paper_id)
        logger.info(f"Publication deleted: {success}")
    
    # Verify deletion
    all_pubs = pub_repo.find_all()
    logger.info(f"Publications after deletion: {len(all_pubs)}")
    
    # Close the connection
    dal_controller._db_manager.close()
    logger.info("Database connection closed")

if __name__ == "__main__":
    main()